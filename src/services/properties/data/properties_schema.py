from bson.objectid import ObjectId
from pydantic import BaseModel, Field
from enum import Enum

from src.database.collection_names import PROPERTIES_SCHEMA_COLLECTION_NAME
from src.database.initiate_database import get_collection_by_name

from src.utils.mongo_object_id import PyObjectId

class DataTypes(Enum):
    STR = 'STR'
    NUMBER = 'NUMBER'
    DATE = 'DATE'
    BOOL = 'BOOL'

class Property(BaseModel):
    name: str = Field(...)
    primitive_type: DataTypes = Field(...)
    validation: str = Field(default=r".{2}")

class PropertiesSchema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    properties: list[Property] = Field(...)
    next_id: PyObjectId | None = Field(...)
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        
get_collection_by_name(PROPERTIES_SCHEMA_COLLECTION_NAME).create_index("name")
get_collection_by_name(PROPERTIES_SCHEMA_COLLECTION_NAME).create_index("next_id")
get_collection_by_name(PROPERTIES_SCHEMA_COLLECTION_NAME).create_index("properties")