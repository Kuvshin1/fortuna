from datetime import datetime
from bson.objectid import ObjectId
from pydantic import BaseModel, Field
from enum import Enum

from src.database.collection_names import USER_COLLECTION_NAME
from src.database.initiate_database import get_collection_by_name

from src.utils.mongo_object_id import PyObjectId


class UserRole(Enum):
    USER = 'USER'
    MODERATOR = 'MODERATOR'
    ADMIN = 'ADMIN'


class UserSchema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    login: str = Field(...)
    role: UserRole = Field(...)
    created_at: datetime = Field(default=datetime.utcnow())

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


get_collection_by_name(USER_COLLECTION_NAME).create_index("login", unique=True)
get_collection_by_name(USER_COLLECTION_NAME).create_index("role")
