from featuremaker.table_engines.pandas_table_engine import PandasTableEngine


def test_pandas_table_engine_inspects_and_previews_csv_with_saved_schema(tmp_path):
    csv_file = tmp_path / "customers.csv"
    csv_file.write_text("customer_id,name\n1,Alice\n,Bob\n", encoding="utf-8")

    table_engine = PandasTableEngine()

    schema_json, row_count = table_engine.inspect_csv(str(csv_file))
    rows = table_engine.preview_csv(str(csv_file), limit=2, schema_json=schema_json)

    assert row_count == 2
    assert schema_json == {
        "columns": [
            {"name": "customer_id", "type": "integer", "nullable": True},
            {"name": "name", "type": "string", "nullable": False},
        ]
    }
    assert rows == [
        {"customer_id": 1, "name": "Alice"},
        {"customer_id": None, "name": "Bob"},
    ]
