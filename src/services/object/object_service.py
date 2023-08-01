import sys
from datetime import datetime
from dateutil.parser import parse
from typing import Any
from src.utils.types.dict import filter_nullable_values_from_dict
from src.services.object.data import object_repository
from src.services.object.data.object_schema import Payload, PayloadData
from src.services.object.data.object_schema import ObjectStatus


def get_objects_by_filter(
    page: int,
    limit: int,
    filtersOr: dict[str, Any] = {},
    filtersAnd: dict[str, Any] = {},
    model_ids: list[str] = [],
    text: str = ''
):
    return object_repository.get_objects(
        page,
        limit,
        filter_nullable_values_from_dict(filtersOr),
        filter_nullable_values_from_dict(filtersAnd),
        model_ids=model_ids,
        text=text
    )


def get_objects_ids_by_filters(filters: dict):
    objects = get_objects_by_filter(
        page=1,
        limit=sys.maxsize,
        filtersAnd=filters
    )
    return list(map(lambda item: str(item.id), objects))


def change_status_objects(action: str, ids: list[str], user_id: str):
    reason = 'Принято в составе пакета' if action == 'approve' else 'Отклонено в составе пакета'
    return object_repository.update_many_objects(
        ids,
        ObjectStatus(
            approve_at=datetime.utcnow() if action =='approve' else None,
            decline_at=datetime.utcnow() if action =='decline' else None,
            moderator_id=user_id,
            reason=reason
        )
    )


def get_count_objects(filtersOr: dict[str, Any], filtersAnd: dict[str, Any]):
    return len(get_objects_by_filter(
        1,
        sys.maxsize,
        filtersOr,
        filtersAnd
    ))

def conversion_to_field_data_type(data_type, value):
    if data_type == "STR":
        return value
    elif data_type == "NUMBER":
        try: 
            int(value)
        except:
            return f"Невозможно преобразовать {value} к числу"
        return int(value)
    elif data_type == "BOOL":
        if value.lower() == "true":
            return True
        elif value.lower() == "false":
            return False
        else:
            return f"Невозможно преобразовать {value} к булевому типу данных"
    elif data_type == "DATE":
        try: 
            date = parse(value)
        except:
            return f"Невозможно преобразовать {value} к дате"
        return date

def csv_to_objects_parser(content: list[dict]):
    object_data = []
    for object in content:
        payload = []
        object_keys_list = list(object.keys())
        property_value = []
        property_name_prev = ''
        for field in object:
            property_name = field.split('|')[1]
            if property_name != property_name_prev and property_name_prev != '':
                payload.append(
                    Payload(property_name=property_name_prev, data=property_value))
                property_value = []
            name = field.split('|')[2]
            value = conversion_to_field_data_type(
                field.split('|')[3],
                object[field].strip()
            )
            property_value.append(PayloadData(name=name, value=value))
            property_name_prev = property_name
            if object_keys_list.index(field) == len(object_keys_list)-1:
                payload.append(
                    Payload(property_name=property_name_prev, data=property_value))
                property_value = []
        object_data.append(payload)
    return object_data
