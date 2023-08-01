from pydantic import BaseModel
from src.utils.mongo_object_id import PyObjectId

class Payload(BaseModel):
    name: str
    types_id: list[str]

class AddModelRequest(BaseModel):
    payload: Payload