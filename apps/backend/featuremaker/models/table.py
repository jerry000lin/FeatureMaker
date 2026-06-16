import enum

import sqlalchemy
from featuremaker.db import Base
from sqlalchemy import BigInteger, Enum, String, Text, DateTime, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, foreign, mapped_column, relationship
from datetime import datetime
from typing import Optional

class SourceType(enum.Enum):
    UPLOAD_FILE = "upload_file"
    WORKFLOW_OUTPUT = "workflow_output"

class StorageType(enum.Enum):
    LOCAL_CSV = "local_csv"

class TableAsset(Base):
    __tablename__ = "table_assets"
    id:Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name:Mapped[str] = mapped_column(String(1024), nullable=False, unique=True)
    description:Mapped[Optional[str]] = mapped_column(Text)
    created_at:Mapped[datetime] = mapped_column(DateTime,server_default=func.now())
    updated_at:Mapped[datetime] = mapped_column(DateTime,server_default=func.now(),onupdate=func.now())
    created_by:Mapped[Optional[str]] = mapped_column(String(255))
    updated_by:Mapped[Optional[str]] = mapped_column(String(255))

    versions:Mapped[list["TableVersion"]] = relationship(
        primaryjoin="TableAsset.id==foreign(TableVersion.table_asset_id)",
        back_populates="table_asset"
    )


class TableVersion(Base):
    __tablename__ = "table_versions"

    __table_args__ = (
        # 联合唯一约束，确保同一数据表资产的版本号唯一
        UniqueConstraint('table_asset_id', 'version_number', name='uq_table_asset_version_number'),
        UniqueConstraint('storage_uri', name='uq_table_asset_storage_uri')
    )

    id:Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    table_asset_id:Mapped[int] = mapped_column(BigInteger, index=True, nullable=False)
    version_number:Mapped[int] = mapped_column(BigInteger, nullable=False,autoincrement=False)
    source_type:Mapped[SourceType] = mapped_column(Enum(SourceType),nullable=False)
    storage_type:Mapped[StorageType] = mapped_column(Enum(StorageType), default=StorageType.LOCAL_CSV, nullable=False)
    storage_uri:Mapped[str] = mapped_column(String(2048), nullable=False)
    schema_json:Mapped[dict] = mapped_column(JSONB, nullable=False)
    row_count:Mapped[int] = mapped_column(BigInteger, nullable=False)
    version:Mapped[str] = mapped_column(String(255), nullable=False)
    description:Mapped[Optional[str]] = mapped_column(Text)
    created_at:Mapped[datetime] = mapped_column(DateTime,server_default=func.now())
    updated_at:Mapped[datetime] = mapped_column(DateTime,server_default=func.now(),onupdate=func.now())
    created_by:Mapped[Optional[str]] = mapped_column(String(255))
    updated_by:Mapped[Optional[str]] = mapped_column(String(255))

    table_asset:Mapped[TableAsset] = relationship(
        primaryjoin="TableAsset.id==foreign(TableVersion.table_asset_id)",
        back_populates="versions"
    )