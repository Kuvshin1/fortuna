from typing import Optional
import bson
import pymongo
from src.utils.mongo_object_id import PyObjectId
from returns.result import Result
from fastapi.encoders import jsonable_encoder
from src.database.collection_names import MODELS_COLLECTION_NAME
from src.database.initiate_database import get_collection_by_name
from src.services.model.data.model_schema import ModelSchema

models_collection = get_collection_by_name(MODELS_COLLECTION_NAME)

def add_model(name: str, types_id: list[PyObjectId]) -> Optional[ModelSchema]:
  model = ModelSchema(id=bson.objectid.ObjectId(), name=name, types_id=types_id, next_id=None)
  model_json = jsonable_encoder(model)
  new_model = models_collection.insert_one(model_json)
  return get_model_by_id(new_model.inserted_id)

def get_actual_model_by_name(name: str) -> Optional[ModelSchema]:
  actual_model = models_collection.find({"name": name}).sort("_id", pymongo.DESCENDING).limit(1)
  actual_model = list(map(ModelSchema.parse_obj, actual_model))
  actual_model = actual_model[0] if len(actual_model) > 0 else None
  return ModelSchema.parse_obj(actual_model) if actual_model is not None else None

def get_models_by_name(name: str) -> list[ModelSchema]:
  models = models_collection.find({"name": name})
  return list(map(ModelSchema.parse_obj, models)) 
   
def get_model_by_id(id: str) -> Optional[ModelSchema]:
  model = models_collection.find_one({"_id": id})
  return ModelSchema.parse_obj(model) if model is not None else None

def update_model(id: str, updated_values: dict) -> ModelSchema:
  models_collection.update_one({'_id': id}, {'$set': updated_values})
  return get_model_by_id(id)

def get_models(page: int, limit: int) -> list[ModelSchema]:
  models = models_collection.find({'next_id': None}).sort("name", pymongo.ASCENDING).skip(limit * (page - 1)).limit(limit)
  return list(map(ModelSchema.parse_obj, models))