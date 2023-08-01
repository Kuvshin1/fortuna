import csv
import os
import sys
from src.config import get_settings
from src.services.model.model_service_schema import AddModelRequest
from src.services.model.data import model_repository
from src.services.properties.data import properties_repository
from src.services.model.data import model_repository
from src.middlewaries.web_auth_middleware import AuthUserBase
from src.services.tokens import token_repository
from src.services.users.data.user_schema import UserRole


def create_sample_csv(id: str):
    model = model_repository.get_model_by_id(id)
    properties_schemas = list(map(lambda item: properties_repository.get_property_by_id(str(item)),model.types_id))
    csv_header = []
    for property_schema in properties_schemas:
        for property in property_schema.properties:
            csv_header_str = '|'.join([model.name, property_schema.name, property.name, property.primitive_type.value])
            csv_header.append(csv_header_str)
    file_path = f'./tmp/models_templates/{id}.csv'
    with open(file_path,'w+',encoding=get_settings().encoding_models_file) as sample_file:
        wr = csv.writer(sample_file)
        wr.writerow(csv_header)
    return file_path


def add_object(request: AddModelRequest):
    previous_version = model_repository.get_actual_model_by_name(request.name) 
    previous_version_id = str(previous_version.id) if previous_version else None

    actual_version_id = str(model_repository.add_model(request.name, request.types_id).id)
    create_sample_csv(actual_version_id)

    if previous_version_id is not None:
        try:
            os.remove(f'./tmp/models_templates/{previous_version_id}.csv')
        except:
            pass
        return model_repository.update_model(previous_version_id, {'next_id': actual_version_id})
    
    return model_repository.get_model_by_id(actual_version_id)


def get_available_models_by_user_id(user: AuthUserBase):
    if user.role == UserRole.ADMIN:
        return model_repository.get_models(page=1, limit=sys.maxsize)
    access_models_id = token_repository.get_token_by_user_id(
            user.id
        ).access_model_kind_names
    return list(filter(
        lambda schema: schema is not None,
        map(
            model_repository.get_actual_model_by_name,
            access_models_id
        )
    ))