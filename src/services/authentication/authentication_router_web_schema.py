from pydantic import BaseModel
from src.utils.form_builder_decorator import as_form

@as_form
class LoginForm(BaseModel):
    login: str
    password: str
