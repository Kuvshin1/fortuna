from fastapi import APIRouter
from returns.pipeline import flow

from src.services.authentication.authentication_router_api_schema import LoginRequest, LoginResponse
from src.services.authentication import authentication_service

from src.services.authentication.authentication_exceptions_http import auth_fail_http_resolver
from src.utils.fp.get_or_else_w import get_or_else_w


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post(
    path="/login",
    response_model=LoginResponse
)
async def login(login_form: LoginRequest) -> LoginResponse:
    return flow(
        authentication_service.login(login_form),
        get_or_else_w(
            on_failure=auth_fail_http_resolver
        )
    )
