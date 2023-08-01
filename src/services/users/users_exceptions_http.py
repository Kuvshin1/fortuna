from fastapi import HTTPException, status
from src.errors.errors import Errors


def user_fail_http_resolver(value: Errors) -> None:
    match value:
        case Errors.USER_DUPLICATE_LOGIN_1002:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=value.value.message,
            )
