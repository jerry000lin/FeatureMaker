from typing import BinaryIO

from sqlalchemy.orm import Session

from featuremaker.repositories.table_asset_repository import TableAssetRepository
from featuremaker.schemas.common import PageParams, PageResponse
from featuremaker.schemas.tables import TableAssetDetail, TableAssetSummary, TablePreviewResponse


class TableAssetNotFoundError(Exception):
    """
    表资产不存在。
    """


class TableAssetInvalidFileTypeError(Exception):
    """
    表资产导入文件类型不合法。
    """


def _validate_file_suffix(file_name: str, allowed_suffixes: tuple[str, ...], message: str) -> None:
    if not file_name.lower().endswith(allowed_suffixes):
        raise TableAssetInvalidFileTypeError(message)


class TableAssetService:
    """
    表资产业务服务。
    """

    def __init__(self, session: Session) -> None:
        self.session = session
        self.repository = TableAssetRepository(session)

    def list_tables(self, page: PageParams) -> PageResponse[TableAssetSummary]:
        """
        查询表资产列表。
        """
        table_assets = self.repository.list(offset=page.offset, limit=page.limit)
        total = self.repository.count()

        return PageResponse[TableAssetSummary](
            items=[TableAssetSummary.model_validate(table_asset) for table_asset in table_assets],
            total=total,
            page=page.page,
            page_size=page.page_size,
        )

    def get_table(self, table_asset_id: int) -> TableAssetDetail:
        """
        查询表资产详情。
        """
        table_asset = self.repository.get_by_id(table_asset_id)
        if table_asset is None:
            raise TableAssetNotFoundError(f"表资产不存在: {table_asset_id}")
        return TableAssetDetail.model_validate(table_asset)

    def import_csv(
        self,
        *,
        file_name: str,
        file_obj: BinaryIO,
        name: str,
        description: str | None,
    ) -> TableAssetDetail:
        """
        导入 CSV 文件并创建表资产。
        """
        _validate_file_suffix(file_name, (".csv",), "只支持上传 CSV 文件")
        raise NotImplementedError("导入 CSV 需要接入 Storage、TableEngine 和 Repository")

    def import_xlsx(
        self,
        *,
        file_name: str,
        file_obj: BinaryIO,
        name: str,
        description: str | None,
    ) -> TableAssetDetail:
        """
        导入 XLSX 文件并创建表资产。
        """
        _validate_file_suffix(file_name, (".xlsx",), "只支持上传 XLSX 文件")
        raise NotImplementedError("导入 XLSX 需要接入 Storage、TableEngine 和 Repository")

    def preview_table(self, table_asset_id: int, limit: int) -> TablePreviewResponse:
        """
        查询表资产预览数据。
        """
        raise NotImplementedError("表预览需要接入 Repository 和 TableEngine")
