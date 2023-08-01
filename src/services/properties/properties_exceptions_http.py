from fastapi import HTTPException, status
from src.errors.errors import Errors

def properties_fail_http_resolver(value: Errors) -> None:
    match value:
        case Errors.DUPLICATE_PROPERTIES_NAME_3001:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=value.value.message)
