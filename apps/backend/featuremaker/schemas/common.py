from typing import Generic, TypeVar

from pydantic import BaseModel, Field

from featuremaker.core.response_code import DEFAULT_MESSAGES, ResponseCode

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """
    平台统一响应结构。
    """

    code: ResponseCode = Field(default=ResponseCode.OK, description="业务响应码")
    message: str = Field(default=DEFAULT_MESSAGES[ResponseCode.OK], description="响应消息")
    data: T | None = Field(default=None, description="响应数据")


def api_success(data: T | None = None) -> ApiResponse[T]:
    """
    构造成功响应。
    """
    return ApiResponse(
        code=ResponseCode.OK,
        message=DEFAULT_MESSAGES[ResponseCode.OK],
        data=data,
    )


def api_error(code: ResponseCode, data: T | None = None, message: str | None = None) -> ApiResponse[T]:
    """
    构造失败响应。
    """
    return ApiResponse(
        code=code,
        message=message or DEFAULT_MESSAGES[code],
        data=data,
    )


class PageParams(BaseModel):
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(10, ge=1, le=100, description="每页数量")

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        return self.page_size


class PageResponse(BaseModel, Generic[T]):
    items: list[T] = Field(..., description="数据列表")
    total: int = Field(..., description="总数")
    page: int = Field(..., description="页码")
    page_size: int = Field(..., description="每页数量")
