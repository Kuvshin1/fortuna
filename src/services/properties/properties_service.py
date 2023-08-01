from src.services.properties.data.properties_schema import Property
from src.services.properties.data import properties_repository

def add_property(name: str, properties: list[Property]):
    previous_version = properties_repository.get_actual_properties_schema_by_name(name) 
    previous_version_id = str(previous_version.id) if previous_version else None

    actual_version_id = str(properties_repository.add_property_schema(name, properties).id)
    
    if previous_version_id is not None:
        properties_repository.update_property_schema(previous_version_id, {'next_id': actual_version_id})
    
    return properties_repository.get_property_by_id(actual_version_id).name