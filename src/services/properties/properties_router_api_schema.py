from pydantic import BaseModel
from src.services.properties.data.properties_schema import Property


class Payload(BaseModel):
    name: str
    properties: list[Property]

class AddPropertySchemaRequest(BaseModel):
    payload: Payload
