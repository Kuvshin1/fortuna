from fastapi import APIRouter, Depends, Request
from src.services.properties.properties_router_api_schema import AddPropertySchemaRequest
from src.services.users.data.user_schema import UserRole
from starlette.authentication import requires
from src.services.properties.data import properties_repository
from src.services.properties import properties_service

router = APIRouter(
    prefix="/properties",
    tags=["properties"],
)

@router.post(
    path="/add",
)
@requires(['authenticated', UserRole.ADMIN])
async def add_property(request: Request, add_property_form: AddPropertySchemaRequest = Depends(AddPropertySchemaRequest)):
    result = properties_service.add_property(
        name=add_property_form.payload.name,
        properties=add_property_form.payload.properties
    )
    return result


@router.get(
    path="/{name}"
)
@requires(['authenticated', UserRole.ADMIN])
async def get_property_by_name(request: Request, name: str):
    return properties_repository.get_properties_by_name(name)


@router.get(
    path="/{id}"
)
@requires(['authenticated', UserRole.ADMIN])
async def get_property_by_id(request: Request, id: str):
    return properties_repository.get_property_by_id(id)