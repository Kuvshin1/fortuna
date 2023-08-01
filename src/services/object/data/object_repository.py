import bson
import pymongo
import re
from typing import Optional, Any
from returns.result import Result
from fastapi.encoders import jsonable_encoder
from src.database.collection_names import OBJECTS_COLLECTION_NAME
from src.database.initiate_database import get_collection_by_name
from src.utils.types_decoder import decode_to_primitive_type
from src.services.object.data.object_schema import Object, ObjectStatus, Payload, PayloadSchemaType

objects_collection = get_collection_by_name(OBJECTS_COLLECTION_NAME)


def add_object(owner_id: str, model_id: str, payload: dict[str, list[Payload]]) -> Result(Object):
    object = Object(
        id=bson.objectid.ObjectId(),
        owner_id=owner_id,
        model_id=model_id,
        status=ObjectStatus(),
        payload=payload
    )
    object_json = jsonable_encoder(object)
    new_object = objects_collection.insert_one(object_json)
    return get_object_by_id(new_object.inserted_id)


def add_many_objects(owner_id: str, model_id: str, payloads: PayloadSchemaType) -> int:
    objects = []
    for payload in payloads:
        object = Object(
            id=bson.objectid.ObjectId(),
            owner_id=owner_id,
            model_id=model_id,
            status=ObjectStatus(),
            payload=payload
        )
        object_json = jsonable_encoder(object)
        objects.append(object_json)
    return len(objects_collection.insert_many(objects).inserted_ids)


def get_object_by_id(id: str) -> Optional[Object]:
    object = objects_collection.find_one({"_id": id})
    return Object.parse_obj(object) if object is not None else None


def update_object(id: str, status: ObjectStatus) -> Optional[Object]:
    objects_collection.update_one(
        {'_id': id}, {'$set': {'status': jsonable_encoder(status)}})
    return get_object_by_id(id)


def update_many_objects(ids: list[str], status: ObjectStatus):
    return objects_collection.update_many({'_id': {'$in': ids}}, {'$set': {'status': jsonable_encoder(status)}}).modified_count


def get_objects(
    page: int,
    limit: int,
    filtersOr: dict[str, Any],
    filtersAnd: dict[str, Any],
    model_ids: list[str],
    text: str
):
    query = {}
    if filtersOr:
        query["$or"] = transform_dict_to_list_filter_or(filtersOr)
    if filtersAnd:
        query["$and"] = transform_dict_to_list_filter_and(filtersAnd)
    if model_ids:
        model_ids_filter = {
            "model_id": {"$in": model_ids}
        }
        if query.get("$and") is None:
            query["$and"] = []
        query["$and"] = [ *query["$and"], model_ids_filter]
    if text:
        query["$text"] = {"$search": text}
    models = objects_collection\
        .find(query)\
        .sort("created_at", pymongo.DESCENDING)\
        .skip((page - 1) * limit)\
        .limit(limit)
    return list(map(Object.parse_obj, models))


def transform_dict_to_list_filter_or(dict_value: dict[str, Any]):
    def decode_primitive_type(value):
        def fnPattern(value): return re.compile(rf'.*{value}.*', re.I)
        value = decode_to_primitive_type(value.lower())
        return {'$regex': fnPattern(value)}

    return [{key: decode_primitive_type(value)} for key, value in dict_value.items()]


def transform_dict_to_list_filter_and(dict_value: dict[str, Any]):
    result = []
    for condition, value in dict_value.items():
        if condition == "date_before":
            result.append(
                {'created_at': {"$gte": decode_to_primitive_type(value.lower())}})
        elif condition == "date_after":
            result.append(
                {'created_at': {"$lte": decode_to_primitive_type(value.lower())}})
        elif condition == "status":
            value = decode_to_status_filter(value)
            result.append({'status.approve_at': value[0]})
            result.append({'status.decline_at': value[1]})
        else:
            result.append(
                {condition: {"$eq": decode_to_primitive_type(value.lower())}})

    return result


def decode_to_status_filter(value):
    if value == 'approved':
        return [{"$ne": None}, {"$eq": None}]
    elif value == 'declined':
        return [{"$eq": None}, {"$ne": None}]
    elif value == 'waiting':
        return [{"$eq": None}, {"$eq": None}]
