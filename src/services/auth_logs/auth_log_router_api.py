import json

from fastapi import APIRouter
from starlette.authentication import requires
from starlette.requests import Request

from src.services.auth_logs.auth_log_router_api_schema import (
    AuthLogsListDtResponse)
from src.services.auth_logs import auth_log_service

router = APIRouter(
    prefix="/auth_logs",
    tags=["auth_logs"],
)


@router.post(
    path="/list/dt",
    response_model=AuthLogsListDtResponse
)
@requires('authenticated', redirect='login')
async def auth_logs_page(request: Request):
    request = json.loads((await request.body()).decode("utf-8"))
    page = request['start'] // request['length'] + 1
    limit = request['length']
    search = request['search']['value'].strip()
    filtersOr = {column['data']: search 
                 for column in request['columns']} if search else {}
    filtersAnd = request['filters']
    logs = auth_log_service.get_auth_logs(
        page=page,
        limit=limit,
        filtersOr=filtersOr,
        filtersAnd=filtersAnd
    )
    count_logs = auth_log_service.get_count_auth_logs(
        filtersOr=filtersOr,
        filtersAnd=filtersAnd
    )
    return AuthLogsListDtResponse(
        data=logs,
        draw=request['draw'],
        recordsTotal=count_logs,
        recordsFiltered=count_logs
    )


# @router.post(
#     path="/list",
#     response_model=AuthLogsListResponse
# )
# async def auth_logs_page(auth_logs_request: AuthLogsListRequest):
#     logs = auth_log_service.get_auth_logs(
#         page=auth_logs_request.start + 1,
#         limit=auth_logs_request.length,
#         filters=auth_logs_request.filters.dict()
#     )
#     return AuthLogsListResponse(
#         data=logs,
#         isNext=len(logs) == auth_logs_request.length,
#         count=len(logs),
#         nextPage=auth_logs_request.start + 1
#     )
