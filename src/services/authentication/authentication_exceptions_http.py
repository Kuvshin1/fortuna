from fastapi import HTTPException, status
from src.errors.errors import Errors


def auth_fail_http_resolver(value: Errors) -> None:
    match value:
        case Errors.USER_NOT_FOUND_1002:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=value.value.message,
                headers={"WWW-Authenticate": "Bearer"},
            )
        case Errors.AUTH_MALFORMED_CREDENTIALS_2001:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=value.value.message
            )
