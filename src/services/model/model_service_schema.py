from pydantic import BaseModel

class AddModelRequest(BaseModel):
    name: str
    types_id: list[str]