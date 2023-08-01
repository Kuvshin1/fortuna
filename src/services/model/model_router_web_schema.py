from pydantic import BaseModel
from src.utils.form_builder_decorator import as_form


@as_form
class AddModelRequest(BaseModel):
    name: str
    types_id: list[str]
