from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from featuremaker.models.table import TableAsset


class TableAssetRepository:
    """
    表资产持久化访问。
    """

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, table_asset_id: int) -> TableAsset | None:
        """
        根据 ID 查询表资产。
        """
        statement = select(TableAsset).where(
            TableAsset.id == table_asset_id,
            TableAsset.deleted_at.is_(None),
        )
        return self.session.scalar(statement)

    def list(self, *, offset: int, limit: int) -> list[TableAsset]:
        """
        分页查询表资产。
        """
        statement = (
            select(TableAsset)
            .where(TableAsset.deleted_at.is_(None))
            .order_by(TableAsset.created_at.desc(), TableAsset.id.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(self.session.scalars(statement).all())

    def count(self) -> int:
        """
        统计表资产总数。
        """
        statement = select(func.count()).select_from(TableAsset).where(TableAsset.deleted_at.is_(None))
        return self.session.scalar(statement) or 0

    def exists_by_name(self, name: str, *, exclude_id: int | None = None) -> bool:
        """
        判断表资产名称是否已存在。
        """
        conditions = [
            TableAsset.name == name,
            TableAsset.deleted_at.is_(None),
        ]
        if exclude_id is not None:
            conditions.append(TableAsset.id != exclude_id)

        statement = (
            select(func.count())
            .select_from(TableAsset)
            .where(*conditions)
        )
        return (self.session.scalar(statement) or 0) > 0

    def create(self, table_asset: TableAsset) -> TableAsset:
        """
        创建表资产记录。
        """
        self.session.add(table_asset)
        self.session.flush()
        return table_asset

    def update(self, table_asset: TableAsset) -> TableAsset:
        """
        更新表资产记录。
        """
        self.session.add(table_asset)
        self.session.flush()
        return table_asset

    def soft_delete(self, table_asset: TableAsset, *, deleted_by: int | None = None) -> TableAsset:
        """
        软删除表资产记录。
        """
        table_asset.deleted_at = datetime.now()
        table_asset.deleted_by = deleted_by
        self.session.add(table_asset)
        self.session.flush()
        return table_asset
