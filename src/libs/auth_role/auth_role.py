from functools import wraps
from fastapi import HTTPException
from starlette import status
from src.errors.errors import Errors
from src.services.users.data.user_schema import UserRole

def role_required(*roles: list[UserRole]):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = kwargs.get('request')
            if not request or request.user.role not in roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=Errors.AUTH_FORBIDDEN_2003.value.message,
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return await func(*args, **kwargs)

        return wrapper
    return decorator
