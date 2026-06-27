from fastapi import APIRouter, Depends, File, Form, Query, UploadFile
from fastapi.responses import JSONResponse

from featuremaker.core.response_code import ResponseCode
from featuremaker.deps import get_table_asset_service
from featuremaker.schemas.common import ApiResponse, PageParams, PageResponse, api_error, api_success
from featuremaker.schemas.tables import TableAssetDetail, TableAssetSummary, TablePreviewResponse
from featuremaker.services.table_service import (
    TableAssetInvalidFileTypeError,
    TableAssetNotFoundError,
    TableAssetService,
)

router = APIRouter(prefix="/tables")


@router.get("", response_model=ApiResponse[PageResponse[TableAssetSummary]])
async def get_tables(
    page: PageParams = Depends(),
    service: TableAssetService = Depends(get_table_asset_service),
):
    """
    获取表资产列表。
    """
    return api_success(data=service.list_tables(page))


@router.post("/import/csv", response_model=ApiResponse[TableAssetDetail])
async def import_csv_table(
    file: UploadFile = File(..., description="上传的 CSV 文件"),
    name: str = Form(..., min_length=1, max_length=255, description="表资产名称"),
    description: str | None = Form(default=None, max_length=1024, description="表资产描述"),
    service: TableAssetService = Depends(get_table_asset_service),
):
    """
    导入 CSV 数据表。
    """
    try:
        table_asset = service.import_csv(
            file_name=file.filename or "uploaded.csv",
            file_obj=file.file,
            name=name,
            description=description,
        )
    except TableAssetInvalidFileTypeError as error:
        return JSONResponse(
            status_code=400,
            content=api_error(ResponseCode.VALIDATION_ERROR, message=str(error)).model_dump(mode="json"),
        )
    return api_success(data=table_asset)


@router.post("/import/xlsx", response_model=ApiResponse[TableAssetDetail])
async def import_xlsx_table(
    file: UploadFile = File(..., description="上传的 XLSX 文件"),
    name: str = Form(..., min_length=1, max_length=255, description="表资产名称"),
    description: str | None = Form(default=None, max_length=1024, description="表资产描述"),
    service: TableAssetService = Depends(get_table_asset_service),
):
    """
    导入 XLSX 数据表。
    """
    try:
        table_asset = service.import_xlsx(
            file_name=file.filename or "uploaded.xlsx",
            file_obj=file.file,
            name=name,
            description=description,
        )
    except TableAssetInvalidFileTypeError as error:
        return JSONResponse(
            status_code=400,
            content=api_error(ResponseCode.VALIDATION_ERROR, message=str(error)).model_dump(mode="json"),
        )
    return api_success(data=table_asset)


@router.get("/{table_asset_id}", response_model=ApiResponse[TableAssetDetail])
async def get_table(
    table_asset_id: int,
    service: TableAssetService = Depends(get_table_asset_service),
):
    """
    获取表资产详情。
    """
    try:
        table_asset = service.get_table(table_asset_id)
    except TableAssetNotFoundError:
        return JSONResponse(
            status_code=404,
            content=api_error(ResponseCode.TABLE_NOT_FOUND).model_dump(mode="json"),
        )
    return api_success(data=table_asset)


@router.get("/{table_asset_id}/preview", response_model=ApiResponse[TablePreviewResponse])
async def get_table_preview(
    table_asset_id: int,
    limit: int = Query(default=20, ge=1, le=100, description="预览行数"),
    service: TableAssetService = Depends(get_table_asset_service),
):
    """
    获取表资产预览。
    """
    try:
        preview = service.preview_table(table_asset_id=table_asset_id, limit=limit)
    except TableAssetNotFoundError:
        return JSONResponse(
            status_code=404,
            content=api_error(ResponseCode.TABLE_NOT_FOUND).model_dump(mode="json"),
        )
    return api_success(data=preview)
