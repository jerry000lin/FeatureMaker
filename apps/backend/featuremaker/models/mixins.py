# models/mixins.py

from datetime import datetime

from sqlalchemy import BigInteger, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column


class AuditMixin:
    """记录数据的创建、更新时间和操作人。"""

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    created_by: Mapped[int | None] = mapped_column(
        BigInteger,
        nullable=True,
    )

    updated_by: Mapped[int | None] = mapped_column(
        BigInteger,
        nullable=True,
    )