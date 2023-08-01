from pydantic import BaseModel
from src.services.users.data.user_schema import UserRole
from src.utils.form_builder_decorator import as_form


class TokenBase(BaseModel):
    access_model_kinds: list[str]


@as_form
class AddUserTokenRequest(TokenBase):
    login: str
    role: UserRole


@as_form
class UpdateUserTokenRequest(TokenBase):
    pass


@as_form
class DeprecateUserTokenRequest(BaseModel):
    deprecated: bool
