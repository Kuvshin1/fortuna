from fastapi import APIRouter, Request
from src.services.tokens.token_repository import get_users_with_some_models_ids
from src.services.users.data.user_schema import UserRole
from starlette.responses import HTMLResponse
from starlette.authentication import requires
from src.services.model.model_service import get_available_models_by_user_id
from src.services.users import users_service
from src.services.object.data import object_repository
from src.services.model.data import model_repository
from src.services.properties.data import properties_repository
from src.services.users.data import users_repository
from src.template import templates


router = APIRouter(
    prefix="/objects",
    tags=["objects"],
)


@router.get(
    path="/",
    response_class=HTMLResponse
)
@requires('authenticated', redirect='login')
async def available_models_page(request: Request, page: int = 1, limit: int = 10):
    available_models_list = get_available_models_by_user_id(
        request.user)

    available_models_count = len(available_models_list)
    all_available_models_page_count = available_models_count // limit + \
        1 if available_models_count % limit else available_models_count // limit

    available_models_list = available_models_list[(
        page - 1) * limit: page * limit]

    return templates.TemplateResponse(
        "/general_pages/objects/available-models-page.html",
        {
            'request': request,
            'available_models_list': available_models_list,
            'current_page': page,
            'all_models_page_count': all_available_models_page_count,
            'add_object_endpoint': "/api/v1/objects/add"
        })


@router.get(
    path="/list",
    response_class=HTMLResponse
)
@requires('authenticated', redirect='login')
async def objects_page(request: Request,
                      model_id: str | None = None,
                      owner_id: str | None = None,
                      date_before: str | None = None,
                      date_after: str | None = None,
                      status: str | None = None):
    models = get_available_models_by_user_id(request.user)
    users = users_service.get_all_users()
    if request.user.role != UserRole.ADMIN:
        users = list(map(users_service.get_user_by_id, get_users_with_some_models_ids([schema.name for schema in models])))
    return templates.TemplateResponse(
        "/general_pages/objects/objects-list.html",
        {"request": request, "users": users, "models": models,
         "model_id": model_id, "owner_id": owner_id,
         "date_before": date_before, "date_after": date_after,
         "status": status}
    )


@router.get(
    path="/add/{id}",
    response_class=HTMLResponse
)
@requires('authenticated', redirect='login')
async def add_object_page(request: Request,  id: str):
    models_schema = model_repository.get_model_by_id(id)

    props = list(map(lambda type_id: properties_repository.get_property_by_id(
        str(type_id)), models_schema.types_id))

    return templates.TemplateResponse(
        "/general_pages/objects/object-add.html",
        {
            'request': request,
            'models_schema': models_schema,
            'types': props,
            'add_object_endpoint': "/api/v1/objects/add"}
    )


@router.get(
    path="/{id}"
)
async def object_page(request: Request, id: str):
    object = object_repository.get_object_by_id(id)
    owner = users_repository.get_user_by_id(str(object.owner_id)).login
    moderator_login = users_repository.get_user_by_id(
        str(object.status.moderator_id)).login if object.status.moderator_id != None else ''
    model = model_repository.get_model_by_id(
        str(object.model_id))
    properties_schemas_id = model.types_id
    properties_schemas = list(map(lambda type_id: properties_repository.get_property_by_id(
        str(type_id)), properties_schemas_id))
    return templates.TemplateResponse(
        "/general_pages/objects/object-content.html", {
            'request': request,
            'object': object,
            'model_name': model.name,
            'properties': properties_schemas,
            'owner': owner,
            'moderator_login': moderator_login
        })
