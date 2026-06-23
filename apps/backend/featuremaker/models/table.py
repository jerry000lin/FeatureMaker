import enum

from featuremaker.models.mixins import AuditMixin
from featuremaker.db import Base
from sqlalchemy import BigInteger, Enum, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional

class SourceType(enum.Enum):
    UPLOAD_FILE = "upload_file"
    WORKFLOW_OUTPUT = "workflow_output"

class StorageType(enum.Enum):
    LOCAL_CSV = "local_csv"

class TableAsset(AuditMixin, Base):
    __tablename__ = "table_assets"
    id:Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name:Mapped[str] = mapped_column(String(1024), nullable=False, unique=True)
    description:Mapped[Optional[str]] = mapped_column(Text)
    source_type:Mapped[SourceType] = mapped_column(Enum(SourceType), nullable=False)
    storage_type:Mapped[StorageType] = mapped_column(Enum(StorageType), nullable=False)
    storage_uri:Mapped[str] = mapped_column(String(1024), nullable=False)
    schema_json:Mapped[dict] = mapped_column(JSONB, nullable=False)
    row_count:Mapped[Optional[int]] = mapped_column(BigInteger)