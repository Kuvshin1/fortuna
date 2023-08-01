import sys
import os
import tempfile
import csv
from fastapi import APIRouter, Request
from src.services.users.data.user_schema import UserRole
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.authentication import requires
from src.template import templates
from src.services.model.data import model_repository
from src.services.model import model_service
from src.services.properties.data import properties_repository
from src.utils.mongo_object_id import PyObjectId
from fastapi.responses import FileResponse


router = APIRouter(
    prefix="/models",
    tags=["models"],
)


@router.get(
    path="/",
    response_class=HTMLResponse
)
@requires(['authenticated', UserRole.ADMIN], redirect='page_404')
async def models_list_page(request: Request, page: int = 1, limit: int = 10):
    models = list(map(lambda item: dict(item), model_repository.get_models(
        page=page,
        limit=limit
    )))

    for i in range(len(models)):
        types = []
        for id in models[i]['types_id']:
            types.append(properties_repository.get_property_by_id(id))
        models[i]['types'] = types

    models_count = len(model_repository.get_models(
        page=1,
        limit=sys.maxsize
    ))
    all_models_page_count = models_count // limit + 1 if models_count % limit else models_count // limit
    return templates.TemplateResponse(
        "/general_pages/settings/models/models-list.html",
        {"request": request, "models": models, 'current_page': page, 'all_models_page_count': all_models_page_count}
    )


@router.get(
    path="/add",
    response_class=HTMLResponse
)
@requires(['authenticated', UserRole.ADMIN], redirect='page_404')
async def add_object_page(request: Request):
    properties = properties_repository.get_properties()
    return templates.TemplateResponse("/general_pages/settings/models/model-add.html", {
        "request": request, 
        "properties": properties,
        "add_models_endpoint": "/api/v1/models/add"})


@router.get(
    path="/{id}/history",
    response_class=HTMLResponse
)
@requires(['authenticated', UserRole.ADMIN], redirect='page_404')
async def history_model_modification(request: Request, id: str):
    model_name = model_repository.get_model_by_id(id).name
    history_model = model_repository.get_models_by_name(model_name)
    history_model.reverse()
    for model_iterarion in range(len(history_model)):
        unpacking_props = list(map(lambda item: properties_repository.get_property_by_id(str(item)), history_model[model_iterarion].types_id))
        history_model[model_iterarion].types_id = unpacking_props
    return templates.TemplateResponse("/general_pages/settings/models/model-history.html", {"request": request, "history": history_model})


@router.get(
    path="/{id}/update", 
    response_class=HTMLResponse
)
@requires(['authenticated', UserRole.ADMIN], redirect='page_404')
async def update_object_page(request: Request, id: str):
    properties = properties_repository.get_properties()
    updated_model = model_repository.get_model_by_id(id)
    return templates.TemplateResponse("/general_pages/settings/models/model-update.html", {
        "request": request, 
        "properties": properties, 
        "updated_model": updated_model,
        "update_models_endpoint": "/api/v1/models/add"})


@router.get(
    path="/{id}",
    response_class=HTMLResponse
)
@requires(['authenticated', UserRole.ADMIN], redirect='page_404')
async def get_object_by_id_page(request: Request, id: PyObjectId):
    model = model_repository.get_model_by_id(str(id))
    if model is None:
        return RedirectResponse('/404', status_code=303)
    types = []
    for type_id in model.types_id:
        property_schema = dict(properties_repository.get_property_by_id(str(type_id)))
        for i in range(len(property_schema['properties'])):
            property_schema['properties'][i] = dict(property_schema['properties'][i])
        types.append(property_schema)
    return templates.TemplateResponse("/general_pages/settings/models/model-page.html",
                                      {"request": request, "model": model, "types": types})


@router.get(
    path="/{id}/sample",
    response_class=HTMLResponse
)
@requires(['authenticated', UserRole.ADMIN], redirect='page_404')
def get_sample_csv(request: Request, id: str):
    model_name = model_repository.get_model_by_id(id).name
    if not os.path.exists('./tmp/models_templates/{id}.csv'):
        model_service.create_sample_csv(id)
    return FileResponse(f'./tmp/models_templates/{id}.csv', filename=f'{model_name}_example.csv', media_type='text/csv')
