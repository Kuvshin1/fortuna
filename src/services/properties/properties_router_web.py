from fastapi import APIRouter, Request
from src.services.users.data.user_schema import UserRole
from starlette.authentication import requires
from src.services.properties.data import properties_repository
from src.template import templates
from starlette.responses import HTMLResponse

router = APIRouter(
    prefix="/properties",
    tags=["properties"],
)


@router.get(
    path="/",
    response_class=HTMLResponse
)
@requires(['authenticated', UserRole.ADMIN], redirect='page_404')
async def properties_list_page(request: Request, page: int = 1, limit: int = 10):
    properties = list(map(lambda item: dict(item), properties_repository.get_properties(
        page=page,
        limit=limit
    )))
    properties_count = len(properties_repository.get_properties())
    all_properties_page_count = properties_count // limit + 1 if properties_count % limit else properties_count // limit
    return templates.TemplateResponse(
        "/general_pages/settings/properties/properties-list.html",
        {"request": request, "properties": properties, 'current_page': page, 'all_properties_page_count': all_properties_page_count}
    )


@router.get(
    path="/add",
    response_class=HTMLResponse
)
@requires(['authenticated', UserRole.ADMIN], redirect='page_404')
async def add_property_page(request: Request):
    return templates.TemplateResponse("/general_pages/settings/properties/property-add.html", {"request": request, "add_property_endpoint": "/api/v1/properties/add"})


@router.get(
    path="/history",
    response_class=HTMLResponse
)
@requires(['authenticated', UserRole.ADMIN], redirect='page_404')
async def history_property_modifications(request: Request, name: str):
    history_property = properties_repository.get_properties_by_name(name)
    history_property.reverse()
    return templates.TemplateResponse("/general_pages/settings/properties/properties-history.html", {"request": request, "history": history_property})


@router.get(
    path="/{id}",
    response_class=HTMLResponse
)
@requires(['authenticated', UserRole.ADMIN], redirect='page_404')
async def update_property_page(request: Request, id: str):
    updated_property_schema = properties_repository.get_property_by_id(id)
    return templates.TemplateResponse("/general_pages/settings/properties/property-update.html", {
        "request": request, 
        "updated_property_schema": updated_property_schema,
        "update_property_endpoint": "/api/v1/properties/add"
        })


@router.get(
    path="/{name}"
)
@requires(['authenticated', UserRole.ADMIN], redirect='page_404')
async def get_property_by_name(request: Request, name: str):
    return properties_repository.get_property_by_name(name)
