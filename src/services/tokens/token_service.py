from src.libs.crypt import hash
from src.services.tokens import token_repository


def add_token(token: str, user_id: str, access_model_kind_names: list[str]):
    token_hash_value = hash.hash(token)

    token = token_repository.add_token(
        user_id=user_id,
        access_model_kind_names=access_model_kind_names,
        value=token_hash_value
    )
    return token
