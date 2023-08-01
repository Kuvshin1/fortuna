import bson
import pymongo
from returns.result import Result
from fastapi.encoders import jsonable_encoder
from src.database.collection_names import PROPERTIES_SCHEMA_COLLECTION_NAME
from src.database.initiate_database import get_collection_by_name
from src.services.properties.data.properties_schema import PropertiesSchema, Property

properies_schemas_collection = get_collection_by_name(PROPERTIES_SCHEMA_COLLECTION_NAME)

def add_property_schema(name: str, properties: list[Property]) ->  Result(PropertiesSchema):
    properties_schema = PropertiesSchema(id=bson.objectid.ObjectId(), name=name, properties=properties, next_id=None)
    properties_schema_json = jsonable_encoder(properties_schema)
    new_schema = properies_schemas_collection.insert_one(properties_schema_json)
    return PropertiesSchema.parse_obj(properies_schemas_collection.find_one({"_id": new_schema.inserted_id}))

def get_actual_properties_schema_by_name(name: str) -> Result(PropertiesSchema | None):
    actual_properties_schema = properies_schemas_collection.find({"name": name}).sort("_id", pymongo.DESCENDING).limit(1)
    actual_properties_schema = list(map(PropertiesSchema.parse_obj, actual_properties_schema))
    actual_properties_schema = actual_properties_schema[0] if len(actual_properties_schema) > 0 else None
    return PropertiesSchema.parse_obj(actual_properties_schema) if actual_properties_schema is not None else None

def get_properties_by_name(name: str) -> Result(list[PropertiesSchema] | None):
    result = properies_schemas_collection.find({"name": name})
    return list(map(PropertiesSchema.parse_obj, result)) if result is not None else None

def get_property_by_id(id: str) -> Result[PropertiesSchema, None]:
    result = properies_schemas_collection.find_one({"_id": id})
    return PropertiesSchema.parse_obj(result) if result is not None else None

def get_properties(page: int = 1, limit: int = 0) -> list[PropertiesSchema]:
    properties = properies_schemas_collection.find({'next_id': None}).sort("name", pymongo.ASCENDING).skip(limit * (page - 1)).limit(limit) if limit == 0 else properies_schemas_collection.find({'next_id': None}).sort("name", pymongo.ASCENDING)
    return list(map(PropertiesSchema.parse_obj, properties))

def update_property_schema(id: str, updated_values: dict) -> Result(PropertiesSchema):
    properies_schemas_collection.update_one({"_id": id}, {'$set': updated_values})
    return get_property_by_id(id)
    