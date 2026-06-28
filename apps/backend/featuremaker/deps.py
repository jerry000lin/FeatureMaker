from featuremaker.config import get_settings
from featuremaker.db import SessionDep
from featuremaker.services.table_service import TableAssetService
from featuremaker.storage.local_table_storage import LocalTableStorage
from featuremaker.table_engines.pandas_table_engine import PandasTableEngine


def get_table_asset_service(session: SessionDep) -> TableAssetService:
    """
    构造表资产业务服务。
    """
    settings = get_settings()
    return TableAssetService(
        session=session,
        storage=LocalTableStorage(settings.table_storage_dir),
        table_engine=PandasTableEngine(),
    )
