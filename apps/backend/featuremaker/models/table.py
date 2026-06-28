import enum
from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, DateTime, Enum, Index, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from featuremaker.db import Base
from featuremaker.models.mixins import AuditMixin

class SourceType(enum.Enum):
    UPLOAD_FILE = "upload_file"
    WORKFLOW_OUTPUT = "workflow_output"

class StorageType(enum.Enum):
    LOCAL_CSV = "local_csv"

class TableAsset(AuditMixin, Base):
    __tablename__ = "table_assets"
    id:Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name:Mapped[str] = mapped_column(String(255), nullable=False)
    description:Mapped[Optional[str]] = mapped_column(Text)
    source_type:Mapped[SourceType] = mapped_column(Enum(SourceType), nullable=False)
    storage_type:Mapped[StorageType] = mapped_column(Enum(StorageType), nullable=False)
    storage_uri:Mapped[str] = mapped_column(String(1024), nullable=False)
    schema_json:Mapped[dict] = mapped_column(JSONB, nullable=False)
    row_count:Mapped[Optional[int]] = mapped_column(BigInteger)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    deleted_by: Mapped[int | None] = mapped_column(BigInteger, nullable=True)

    __table_args__ = (
        Index(
            "uq_table_assets_name_active",
            "name",
            unique=True,
            postgresql_where=deleted_at.is_(None),
        ),
    )
