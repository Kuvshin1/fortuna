from pydantic import BaseModel

from src.services.auth_logs.data.auth_log_schema import AuthLogSchema


class AuthLogsFilter(BaseModel):
    login: str | None
    success: bool | None
    client_type: str | None


class AuthLogsListRequest(BaseModel):
    start: int
    length: int
    filters: AuthLogsFilter


class AuthLogsListResponse(BaseModel):
    isNext: bool
    count: int
    nextPage: int
    data: list[AuthLogSchema]


class AuthLogsListDtResponse(BaseModel):
    data: list[AuthLogSchema]
    draw: int
    recordsTotal: int
    recordsFiltered: int | None
