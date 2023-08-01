from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from src.services.object.data.object_schema import ObjectStatus, PayloadSchemaType
from src.services.object.data.object_schema import Payload
from src.types.pagination import ListRequest 
from src.utils.mongo_object_id import PyObjectId


class Payload(BaseModel):
    model_id: str
    properties: PayloadSchemaType


class AddObjectRequest(BaseModel):
    payload: Payload


class Object(BaseModel):
    id: PyObjectId
    created_at: datetime
    status: ObjectStatus
    owner_id: str
    model_id: str
    payload: Optional[PayloadSchemaType] = []


class ObjectDt(Object):
    model_name: str


class ObjectDtResponse(BaseModel):
    data: list[ObjectDt]
    draw: int
    recordsTotal: int
    recordsFiltered: int | None


class DeclineObjectRequest(BaseModel):
    id: str
    reason: str | None


class GetObjectsRequest(ListRequest):
    text: str
