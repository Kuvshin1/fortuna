from fastapi import APIRouter, Request
from starlette.responses import HTMLResponse
from starlette.authentication import requires
from src.template import templates

router = APIRouter(
    prefix="/search",
    tags=["search"],
)


@router.get(
    path="/",
    response_class=HTMLResponse
)
@requires('authenticated', redirect='login')
async def search_page(request: Request):
    return templates.TemplateResponse(
        "/general_pages/search/index.html",
        {
            'request': request,
        }
    )
