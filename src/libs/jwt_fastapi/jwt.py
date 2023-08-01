from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from starlette import status

from src.config import get_settings
from src.errors.errors import Errors
from src.services.users.data import users_repository
from src.services.users.data.user_schema import UserSchema


class JWTPayloadData(BaseModel):
    user_id: str


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        get_settings().secret_key,
        algorithm=get_settings().algorithm
    )
    return encoded_jwt


def get_current_user(
        token: str = Depends(oauth2_scheme)
) -> UserSchema:
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=Errors.AUTH_INVALID_TOKEN_2002,
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = users_repository.get_user_by_id(
        payload.user_id
    )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=Errors.AUTH_INVALID_TOKEN_2002,
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def decode_token(token: str):
    try:
        payload = jwt.decode(
            token,
            get_settings().secret_key,
            algorithms=[get_settings().algorithm]
        )
        return JWTPayloadData(
            user_id=payload.get('user_id')
        )
    except JWTError:
        return None
