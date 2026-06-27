from featuremaker.db import SessionDep
from featuremaker.services.table_service import TableAssetService


def get_table_asset_service(session: SessionDep) -> TableAssetService:
    """
    构造表资产业务服务。
    """
    return TableAssetService(session)
