from enum import StrEnum


class ResponseCode(StrEnum):
    """
    平台统一业务响应码。
    """

    OK = "OK"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    NOT_FOUND = "NOT_FOUND"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    TABLE_NOT_FOUND = "TABLE_NOT_FOUND"
    TABLE_NAME_EXISTS = "TABLE_NAME_EXISTS"


DEFAULT_MESSAGES: dict[ResponseCode, str] = {
    ResponseCode.OK: "成功",
    ResponseCode.VALIDATION_ERROR: "参数校验错误",
    ResponseCode.NOT_FOUND: "资源不存在",
    ResponseCode.INTERNAL_ERROR: "服务内部错误",
    ResponseCode.TABLE_NOT_FOUND: "表资产不存在",
    ResponseCode.TABLE_NAME_EXISTS: "表资产名称已存在",
}
