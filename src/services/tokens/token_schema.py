import pymongo
from datetime import datetime
from bson.objectid import ObjectId
from pydantic import BaseModel, Field
from src.database.collection_names import TOKEN_COLLECTION_NAME
from src.database.initiate_database import get_collection_by_name

from src.utils.mongo_object_id import PyObjectId


class TokenSchema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: str = Field(...)
    value: str = Field(...)
    access_model_kind_names: list[str] = Field(...)
    created_at: datetime = Field(default=datetime.utcnow())
    deprecated: bool = Field(default=False)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


get_collection_by_name(TOKEN_COLLECTION_NAME).create_index([("user_id", pymongo.DESCENDING)])
get_collection_by_name(TOKEN_COLLECTION_NAME).create_index([("created_at", pymongo.DESCENDING)])