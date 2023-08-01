from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    host: str
    port: int

    api_prefix: str

    mongo_uri: str
    db_name: str

    secret_key: str
    algorithm: str

    access_token_expire_minutes: int
    
    encoding_models_file: str

    class Config:
        env_file = "./.env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
