from typing import Optional
import bson
import pymongo
from returns.result import Result, Success, Failure
from fastapi.encoders import jsonable_encoder
from src.database.collection_names import USER_COLLECTION_NAME
from src.database.initiate_database import get_collection_by_name
from src.errors.errors import Errors
from src.services.users.data.user_schema import UserRole, UserSchema

users_collection = get_collection_by_name(USER_COLLECTION_NAME)


def add_user(login: str, role: UserRole) -> Result[UserSchema, Errors]:
    user = UserSchema(id=bson.objectid.ObjectId(), login=login, role=role)
    user_json = jsonable_encoder(user)
    try:
        new_user = users_collection.insert_one(user_json)
    except pymongo.errors.DuplicateKeyError:
        return Failure(Errors.USER_DUPLICATE_LOGIN_1002)
    return Success(UserSchema.parse_obj(users_collection.find_one({"_id": new_user.inserted_id})))


def get_user_by_login(login: str) -> Optional[UserSchema]:
    user = users_collection.find_one({"login": login})
    return UserSchema.parse_obj(user) if user is not None else None


def get_user_by_id(id: str) -> Optional[UserSchema]:
    user = users_collection.find_one({"_id": id})
    return UserSchema.parse_obj(user) if user is not None else None


def get_users(page: int, limit: int) -> list[UserSchema]:
    users = users_collection.find().sort("role", pymongo.ASCENDING).skip(limit * (page - 1)).limit(limit)
    return list(map(UserSchema.parse_obj, users))
