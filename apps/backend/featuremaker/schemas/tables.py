from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from featuremaker.models.table import SourceType, StorageType


class TableColumnSchema(BaseModel):
    """
    数据表中的一个字段。
    """

    name: str = Field(..., description="字段名")
    type: str = Field(..., description="字段类型")
    nullable: bool = Field(..., description="是否允许为空")


class TableSchema(BaseModel):
    """
    表结构元数据。
    """

    model_config = ConfigDict(extra="allow")

    columns: list[TableColumnSchema] = Field(default_factory=list, description="表字段列表")


class TableAssetSummary(BaseModel):
    """
    表资产列表中的单条数据。
    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="表资产 ID")
    name: str = Field(..., description="表资产名称")
    description: str | None = Field(default=None, description="表资产描述")
    source_type: SourceType = Field(..., description="来源类型")
    storage_type: StorageType = Field(..., description="存储类型")
    row_count: int | None = Field(default=None, description="表行数")
    created_at: datetime = Field(..., description="创建时间")


class TableAssetDetail(TableAssetSummary):
    """
    表资产详情。
    """

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    # schema_json 会与 Pydantic BaseModel 的历史方法名冲突，内部使用 table_schema 避开，
    # 对外仍通过 alias 保持接口字段名为 schema_json。
    table_schema: TableSchema = Field(
        default_factory=TableSchema,
        validation_alias="schema_json",
        serialization_alias="schema_json",
        description="表结构元数据",
    )


class TablePreviewResponse(BaseModel):
    """
    表预览数据。
    """

    model_config = ConfigDict(populate_by_name=True)

    id: int = Field(..., description="表资产 ID")
    # schema_json 会与 Pydantic BaseModel 的历史方法名冲突，内部使用 table_schema 避开，
    # 对外仍通过 alias 保持接口字段名为 schema_json。
    table_schema: TableSchema = Field(
        default_factory=TableSchema,
        validation_alias="schema_json",
        serialization_alias="schema_json",
        description="表结构元数据",
    )
    rows: list[dict[str, Any]] = Field(default_factory=list, description="表预览数据")
    row_count: int = Field(default=0, description="表总行数")
