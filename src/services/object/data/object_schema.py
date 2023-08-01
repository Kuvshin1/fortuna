import pymongo
from datetime import datetime
from bson.objectid import ObjectId
from pydantic import BaseModel, Field

from src.database.collection_names import OBJECTS_COLLECTION_NAME
from src.database.initiate_database import get_collection_by_name

from src.utils.mongo_object_id import PyObjectId


class ObjectStatus(BaseModel):
    approve_at: datetime | None = Field(default=None)
    decline_at: datetime | None = Field(default=None)
    reason: str | None = Field(default=None)
    moderator_id: str |None = Field(default=None)

class PayloadData(BaseModel):
    name: str = Field(...)
    value: str | int | datetime | bool | None = Field(...)

class Payload(BaseModel):
    property_name: str
    data: list[PayloadData]

PayloadSchemaType = list[Payload]

class Object(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default=datetime.utcnow())
    status: ObjectStatus
    owner_id: PyObjectId = Field(...)
    model_id: PyObjectId = Field(...)
    payload: PayloadSchemaType = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


get_collection_by_name(OBJECTS_COLLECTION_NAME).create_index("model_id")
get_collection_by_name(OBJECTS_COLLECTION_NAME).create_index("created_at")
get_collection_by_name(OBJECTS_COLLECTION_NAME).create_index("owner_id")
get_collection_by_name(OBJECTS_COLLECTION_NAME).create_index([("status.approve_at", pymongo.DESCENDING), ("status.decline_at", pymongo.DESCENDING)])
get_collection_by_name(OBJECTS_COLLECTION_NAME).create_index([("payload.data.value", pymongo.TEXT)])
