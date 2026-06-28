from datetime import datetime
from collections.abc import Iterator
from typing import BinaryIO

import pytest
from fastapi.testclient import TestClient

from featuremaker.deps import get_table_asset_service
from featuremaker.main import app
from featuremaker.models.table import SourceType, StorageType
from featuremaker.schemas.common import PageParams, PageResponse
from featuremaker.schemas.tables import (
    TableColumnSchema,
    TableAssetDeleteRequest,
    TableAssetDeleteResponse,
    TableAssetDetail,
    TableAssetSummary,
    TableAssetUpdateRequest,
    TablePreviewResponse,
    TableSchema,
)
from featuremaker.services.table_service import (
    TableAssetInvalidFileTypeError,
    TableAssetNameExistsError,
    TableAssetNotFoundError,
)


class FakeTableAssetService:
    def _fake_table(self, table_asset_id: int, name: str) -> TableAssetDetail:
        return TableAssetDetail(
            id=table_asset_id,
            name=name,
            description=None,
            source_type=SourceType.UPLOAD_FILE,
            storage_type=StorageType.LOCAL_CSV,
            row_count=0,
            created_at=datetime.now(),
            table_schema=TableSchema(),
        )

    def list_tables(self, page: PageParams) -> PageResponse[TableAssetSummary]:
        return PageResponse[TableAssetSummary](
            items=[],
            total=0,
            page=page.page,
            page_size=page.page_size,
        )

    def get_table(self, table_asset_id: int) -> TableAssetDetail:
        if table_asset_id == 404:
            raise TableAssetNotFoundError("表资产不存在")
        return self._fake_table(table_asset_id, "customers")

    def import_csv(
        self,
        *,
        file_name: str,
        file_obj: BinaryIO,
        name: str,
        description: str | None,
    ) -> TableAssetDetail:
        if not file_name.lower().endswith(".csv"):
            raise TableAssetInvalidFileTypeError("只支持上传 CSV 文件")
        return self._fake_table(1, name)

    def import_xlsx(
        self,
        *,
        file_name: str,
        file_obj: BinaryIO,
        name: str,
        description: str | None,
    ) -> TableAssetDetail:
        if not file_name.lower().endswith(".xlsx"):
            raise TableAssetInvalidFileTypeError("只支持上传 XLSX 文件")
        return self._fake_table(2, name)

    def preview_table(self, table_asset_id: int, limit: int) -> TablePreviewResponse:
        return TablePreviewResponse(
            id=table_asset_id,
            table_schema=TableSchema(),
            rows=[],
            row_count=0,
        )

    def update_table(self, request: TableAssetUpdateRequest) -> TableAssetDetail:
        if request.id == 404:
            raise TableAssetNotFoundError("表资产不存在")
        if request.name == "exists":
            raise TableAssetNameExistsError("表资产名称已存在")
        return self._fake_table(request.id, request.name or "customers")

    def delete_table(self, request: TableAssetDeleteRequest) -> TableAssetDeleteResponse:
        if request.id == 404:
            raise TableAssetNotFoundError("表资产不存在")
        return TableAssetDeleteResponse(id=request.id, name="customers")


@pytest.fixture
def client() -> Iterator[TestClient]:
    app.dependency_overrides[get_table_asset_service] = lambda: FakeTableAssetService()
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def test_get_table_preview_api(client: TestClient):
    response = client.get("/tables/123/preview")

    assert response.status_code == 200

    body = response.json()
    assert body["code"] == "OK"
    assert body["message"] == "成功"
    assert body["data"]["id"] == 123
    assert body["data"]["schema_json"] == {"columns": []}
    assert body["data"]["rows"] == []
    assert body["data"]["row_count"] == 0


def test_table_preview_response_accepts_internal_table_schema_name():
    preview = TablePreviewResponse(
        id=1,
        table_schema=TableSchema(
            columns=[TableColumnSchema(name="customer_id", type="integer", nullable=True)],
        ),
        rows=[],
        row_count=0,
    )

    assert preview.model_dump(by_alias=True)["schema_json"] == {
        "columns": [{"name": "customer_id", "type": "integer", "nullable": True}]
    }


def test_get_tables_api(client: TestClient):
    response = client.get("/tables")

    assert response.status_code == 200

    body = response.json()
    assert body["code"] == "OK"
    assert body["message"] == "成功"
    assert isinstance(body["data"], dict)
    assert body["data"]["items"] == []
    assert body["data"]["total"] == 0
    assert body["data"]["page"] == 1
    assert body["data"]["page_size"] == 10


def test_import_csv_table_api(client: TestClient):
    response = client.post(
        "/tables/import/csv",
        data={"name": "customers"},
        files={"file": ("customers.csv", b"customer_id,name\n1,Alice\n", "text/csv")},
    )

    assert response.status_code == 200

    body = response.json()
    assert body["code"] == "OK"
    assert body["message"] == "成功"
    assert body["data"]["id"] == 1
    assert body["data"]["name"] == "customers"


def test_import_csv_table_rejects_non_csv(client: TestClient):
    response = client.post(
        "/tables/import/csv",
        data={"name": "customers"},
        files={"file": ("customers.xlsx", b"not csv", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
    )

    assert response.status_code == 400

    body = response.json()
    assert body["code"] == "VALIDATION_ERROR"
    assert body["message"] == "只支持上传 CSV 文件"
    assert body["data"] is None


def test_import_xlsx_table_api(client: TestClient):
    response = client.post(
        "/tables/import/xlsx",
        data={"name": "customers_xlsx"},
        files={
            "file": (
                "customers.xlsx",
                b"fake xlsx bytes",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        },
    )

    assert response.status_code == 200

    body = response.json()
    assert body["code"] == "OK"
    assert body["message"] == "成功"
    assert body["data"]["id"] == 2
    assert body["data"]["name"] == "customers_xlsx"


def test_get_table_api(client: TestClient):
    response = client.get("/tables/123")

    assert response.status_code == 200

    body = response.json()
    assert body["code"] == "OK"
    assert body["message"] == "成功"
    assert body["data"]["id"] == 123
    assert body["data"]["name"] == "customers"
    assert body["data"]["schema_json"] == {"columns": []}


def test_get_table_not_found_api(client: TestClient):
    response = client.get("/tables/404")

    assert response.status_code == 404

    body = response.json()
    assert body["code"] == "TABLE_NOT_FOUND"
    assert body["message"] == "表资产不存在"
    assert body["data"] is None


def test_update_table_api(client: TestClient):
    response = client.post(
        "/tables/update",
        json={"id": 123, "name": "customers_v2", "description": None},
    )

    assert response.status_code == 200

    body = response.json()
    assert body["code"] == "OK"
    assert body["message"] == "成功"
    assert body["data"]["id"] == 123
    assert body["data"]["name"] == "customers_v2"


def test_update_table_not_found_api(client: TestClient):
    response = client.post("/tables/update", json={"id": 404, "name": "customers_v2"})

    assert response.status_code == 404

    body = response.json()
    assert body["code"] == "TABLE_NOT_FOUND"
    assert body["message"] == "表资产不存在"
    assert body["data"] is None


def test_update_table_rejects_duplicate_name(client: TestClient):
    response = client.post("/tables/update", json={"id": 123, "name": "exists"})

    assert response.status_code == 400

    body = response.json()
    assert body["code"] == "TABLE_NAME_EXISTS"
    assert body["message"] == "表资产名称已存在"
    assert body["data"] is None


def test_delete_table_api(client: TestClient):
    response = client.post("/tables/delete", json={"id": 123})

    assert response.status_code == 200

    body = response.json()
    assert body["code"] == "OK"
    assert body["message"] == "成功"
    assert body["data"] == {"id": 123, "name": "customers"}


def test_delete_table_not_found_api(client: TestClient):
    response = client.post("/tables/delete", json={"id": 404})

    assert response.status_code == 404

    body = response.json()
    assert body["code"] == "TABLE_NOT_FOUND"
    assert body["message"] == "表资产不存在"
    assert body["data"] is None
