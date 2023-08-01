from datetime import datetime
from src.services.users.data.user_schema import UserRole
from starlette.authentication import (
    AuthCredentials, AuthenticationBackend, AuthenticationError, BaseUser
)

from src.libs.jwt_fastapi.jwt import get_current_user


class AuthUserBase(BaseUser):
  id: str
  login: str


class AuthUserBase(BaseUser):
    def __init__(self, id: str, login: str, role: UserRole, created_at: datetime) -> None:
        self.id = id
        self.login = login
        self.role = role
        self.created_at = created_at

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def get_id(self) -> str:
        return self.id

    @property
    def get_login(self) -> str:
        return self.login
    
    @property
    def get_role(self) -> UserRole:
        return self.role
    
    @property
    def get_created_at(self) -> datetime:
        return self.created_at


class AuthMiddleware(AuthenticationBackend):
    async def authenticate(self, conn):
        auth = None

        if "Authorization" in conn.cookies:
            auth = conn.cookies.get("Authorization")
        elif "Authorization" in conn.headers:
            auth = conn.headers.get("Authorization")
        else:
            return
        
        try:
            scheme, token = auth.split()
            if scheme.lower() != 'bearer':
                return
            user = get_current_user(token)
        except:
            raise AuthenticationError('Invalid basic auth credentials')
        return AuthCredentials(["authenticated", user.role]), AuthUserBase(str(user.id), user.login, user.role, user.created_at)
