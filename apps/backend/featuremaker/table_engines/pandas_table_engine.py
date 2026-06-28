from pathlib import Path
from typing import Any

import pandas as pd


class PandasTableEngine:
    """
    基于 pandas 的本地表读取能力。
    """

    def inspect_csv(self, storage_uri: str) -> tuple[dict, int]:
        df = pd.read_csv(Path(storage_uri))
        schema_json = {
            "columns": [
                {
                    "name": str(column_name),
                    "type": self._normalize_series_dtype(df[column_name]),
                    "nullable": bool(df[column_name].isna().any()),
                }
                for column_name in df.columns
            ]
        }
        return schema_json, len(df)

    def preview_csv(
        self,
        storage_uri: str,
        *,
        limit: int,
        schema_json: dict | None = None,
    ) -> list[dict[str, Any]]:
        read_options = self._build_read_options(schema_json)
        df = pd.read_csv(Path(storage_uri), nrows=limit, **read_options)
        return [
            {column: self._normalize_value(value) for column, value in row.items()}
            for row in df.to_dict(orient="records")
        ]

    def _build_read_options(self, schema_json: dict | None) -> dict[str, Any]:
        if not schema_json:
            return {}

        dtypes: dict[str, str] = {}
        parse_dates: list[str] = []
        for column in schema_json.get("columns", []):
            column_name = column.get("name")
            column_type = column.get("type")
            if not column_name or not column_type:
                continue

            if column_type == "integer":
                dtypes[column_name] = "Int64"
            elif column_type == "float":
                dtypes[column_name] = "Float64"
            elif column_type == "boolean":
                dtypes[column_name] = "boolean"
            elif column_type == "string":
                dtypes[column_name] = "string"
            elif column_type == "datetime":
                parse_dates.append(column_name)

        options: dict[str, Any] = {}
        if dtypes:
            options["dtype"] = dtypes
        if parse_dates:
            options["parse_dates"] = parse_dates
        return options

    def _normalize_series_dtype(self, series: pd.Series) -> str:
        dtype = series.dtype
        if pd.api.types.is_integer_dtype(dtype):
            return "integer"
        if pd.api.types.is_float_dtype(dtype) and self._is_nullable_integer(series):
            return "integer"
        if pd.api.types.is_float_dtype(dtype):
            return "float"
        if pd.api.types.is_bool_dtype(dtype):
            return "boolean"
        if pd.api.types.is_datetime64_any_dtype(dtype):
            return "datetime"
        return "string"

    def _is_nullable_integer(self, series: pd.Series) -> bool:
        non_null_values = series.dropna()
        if non_null_values.empty:
            return False
        return bool((non_null_values % 1 == 0).all())

    def _normalize_value(self, value: Any) -> Any:
        if pd.isna(value):
            return None
        if isinstance(value, pd.Timestamp):
            return value.isoformat()
        if hasattr(value, "item"):
            return value.item()
        return value
