from datetime import timedelta

from returns.result import Result, Success, Failure

from src.config import get_settings
from src.errors.errors import Errors
from src.libs.crypt.hash import verify
from src.libs.jwt_fastapi.jwt import JWTPayloadData, create_access_token

from .authentication_service_model import (LoginRequest, TokenModel, ClientInformation)
from src.services.auth_logs import auth_log_service
from src.services.users.data import users_repository
from src.services.tokens import token_repository


def login(request: LoginRequest, metadata: ClientInformation | None = None) -> Result[TokenModel, Errors]:
    user = users_repository.get_user_by_login(request.login)
    if user is None:
        auth_log_service.add_auth_log_failed(
            login=request.login,
            password=request.password,
            ip=metadata.ip,
            user_agent=metadata.user_agent,
            reason=Errors.USER_NOT_FOUND_1002.value.message
        )
        return Failure(Errors.USER_NOT_FOUND_1002)
    user_id = str(user.id)
    token = token_repository.get_token_by_user_id(user_id)
    if token is None or token.deprecated or not verify(request.password, token.value):
        auth_log_service.add_auth_log_failed(
            login=request.login,
            password=request.password,
            ip=metadata.ip,
            user_agent=metadata.user_agent,
            reason=Errors.AUTH_MALFORMED_CREDENTIALS_2001.value.message
        )
        return Failure(Errors.AUTH_MALFORMED_CREDENTIALS_2001)
    access_token_expires = timedelta(minutes=get_settings().access_token_expire_minutes)
    payload: JWTPayloadData = JWTPayloadData(
        user_id=user_id
    )
    access_token = create_access_token(
        data=payload.dict(),
        expires_delta=access_token_expires
    )
    auth_log_service.add_auth_log_success(
        login=request.login,
        password_id=str(token.id),
        ip=metadata.ip,
        user_agent=metadata.user_agent,
    )
    return Success(TokenModel(access_token=access_token, token_type="bearer"))
