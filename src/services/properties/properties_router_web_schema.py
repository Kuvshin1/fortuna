from pydantic import BaseModel
from src.services.properties.data.properties_schema import Property

class AddPropertySchemaRequest(BaseModel):
    name: str
    properties: list[Property]
