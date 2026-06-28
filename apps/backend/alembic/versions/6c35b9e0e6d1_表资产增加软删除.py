"""表资产增加软删除

Revision ID: 6c35b9e0e6d1
Revises: cdb19e894181
Create Date: 2026-06-28 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6c35b9e0e6d1"
down_revision: Union[str, Sequence[str], None] = "cdb19e894181"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("table_assets", sa.Column("deleted_at", sa.DateTime(), nullable=True))
    op.add_column("table_assets", sa.Column("deleted_by", sa.BigInteger(), nullable=True))
    op.drop_constraint("table_assets_name_key", "table_assets", type_="unique")
    op.create_index(
        "uq_table_assets_name_active",
        "table_assets",
        ["name"],
        unique=True,
        postgresql_where=sa.text("deleted_at IS NULL"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("uq_table_assets_name_active", table_name="table_assets")
    op.create_unique_constraint("table_assets_name_key", "table_assets", ["name"])
    op.drop_column("table_assets", "deleted_by")
    op.drop_column("table_assets", "deleted_at")
