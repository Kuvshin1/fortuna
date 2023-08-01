import re
from typing import Any

import pymongo
from fastapi.encoders import jsonable_encoder
from src.database.collection_names import AUTH_LOG_COLLECTION_NAME
from src.database.initiate_database import get_collection_by_name
from src.services.auth_logs.data.auth_log_schema import AuthLogSchema, PasswordData
from src.utils.types_decoder import decode_to_primitive_type

auth_logs_collection = get_collection_by_name(AUTH_LOG_COLLECTION_NAME)


def add_auth_log(login: str, ip: str, success: bool, password: PasswordData, user_agent: str, reason: str | None):
    auth_log = AuthLogSchema(
        login=login,
        password=password,
        success=success,
        reason=reason,
        ip=ip,
        user_agent=user_agent
    )
    auth_log_json = jsonable_encoder(auth_log)
    return auth_logs_collection.insert_one(auth_log_json)


def get_auth_logs(page: int, limit: int, filtersOr: dict[str, Any], filtersAnd: dict[str, Any]):
    filters = {}
    if filtersOr:
        filters["$or"] = transform_dict_to_list_filter_or(filtersOr)
    if filtersAnd:
        filters["$and"] = transform_dict_to_list_filter_and(filtersAnd)
    logs = auth_logs_collection\
        .find(filters)\
        .sort("created_at", pymongo.DESCENDING)\
        .skip((page - 1) * limit)\
        .limit(limit)
    return list(map(AuthLogSchema.parse_obj, logs))


def transform_dict_to_list_filter_or(dict_value: dict[str, Any]):
    def decode_primitive_type(value):
        fnPattern = lambda value: re.compile(rf'.*{value}.*', re.I)
        
        value = decode_to_primitive_type(value.lower())
        return {'$regex': fnPattern(value)}

    return [{key: decode_primitive_type(value)} for key, value in dict_value.items()]


def transform_dict_to_list_filter_and(dict_value: dict[str, Any]):
    def decode_primitive_type(value):
        value = decode_to_primitive_type(value.lower())
        return {'$eq': value}

    return [{key: decode_primitive_type(value)} for key, value in dict_value.items()]
