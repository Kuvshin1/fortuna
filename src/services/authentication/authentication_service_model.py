from pydantic import BaseModel


class LoginRequest(BaseModel):
    login: str
    password: str


class ClientInformation(BaseModel):
    ip: str
    user_agent: str


class TokenModel(BaseModel):
    access_token: str
    token_type: str
