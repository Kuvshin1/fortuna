from pymongo import MongoClient
from src.config import get_settings
from src.database.collection_names import list_collections

settings = get_settings()

mongodb_client = MongoClient(settings.mongo_uri)

def initiate_database():
  initiate_collections()
  return mongodb_client

def initiate_collections():
  database = mongodb_client[settings.db_name]
  for collection_name in list_collections:
    database[collection_name]

def get_collection_by_name(collection_name):
  database = mongodb_client[settings.db_name]
  if collection_name not in list_collections:
    raise Exception(f"Collection with name '{collection_name}' not exist")
  return database[collection_name]
