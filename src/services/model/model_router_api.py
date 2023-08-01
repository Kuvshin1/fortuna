from fastapi import APIRouter, Depends, Request
from src.services.model.model_router_api_schema import AddModelRequest
from src.services.users.data.user_schema import UserRole
from starlette.authentication import requires
from src.services.model import model_service
from src.services.model.data import model_repository


router = APIRouter(
    prefix="/models",
    tags=["models"],
)

@router.post(
    path="/add"
)
@requires(['authenticated', UserRole.ADMIN])
async def add_object(request: Request, add_object_form: AddModelRequest = Depends(AddModelRequest)):
    result = model_service.add_object(add_object_form.payload)
    return result


@router.get(
    path="/{name}"
)
@requires(['authenticated', UserRole.ADMIN])
async def get_model(request: Request, name: str):
    return model_repository.get_actual_model_by_name(name)


@router.get(
    path="/{id}"
)
@requires(['authenticated', UserRole.ADMIN])
async def get_object_by_id(request: Request, id: str):
    return model_repository.get_object_by_id(id)