from bson.objectid import ObjectId
from pydantic import BaseModel, Field

from src.utils.mongo_object_id import PyObjectId
from src.database.collection_names import MODELS_COLLECTION_NAME
from src.database.initiate_database import get_collection_by_name

class ModelSchema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    types_id: list[PyObjectId] = Field(...)
    next_id: PyObjectId | None = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

get_collection_by_name(MODELS_COLLECTION_NAME).create_index("name")
get_collection_by_name(MODELS_COLLECTION_NAME).create_index("next_id")
get_collection_by_name(MODELS_COLLECTION_NAME).create_index("types_id")