from pydantic import BaseModel
from src.services.properties_data.data.properties_data_schema import Payload 

class Payload(BaseModel):
    model_id: str
    properties: dict[str, list[Payload]]

class AddObjectRequest(BaseModel):
    payload: Payload