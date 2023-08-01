import pydantic
import pymongo
from datetime import datetime
from bson.objectid import ObjectId
from pydantic import BaseModel, Field
from src.database.collection_names import AUTH_LOG_COLLECTION_NAME
from src.database.initiate_database import get_collection_by_name
from src.utils.mongo_object_id import PyObjectId

# bug reference: https://github.com/tiangolo/fastapi/issues/1515#issuecomment-782835977
pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str


class PasswordData(BaseModel):
    id: str | None
    value: str | None


class AuthLogSchema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    login: str = Field(...)
    password: PasswordData = Field(...)
    success: bool = Field(...)
    reason: str | None = Field(...)
    user_agent: str = Field(...)
    ip: str = Field(...)
    created_at: datetime = Field(default=datetime.utcnow())

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


get_collection_by_name(AUTH_LOG_COLLECTION_NAME).create_index([("login", pymongo.ASCENDING)])
get_collection_by_name(AUTH_LOG_COLLECTION_NAME).create_index([("created_at", pymongo.DESCENDING)])
