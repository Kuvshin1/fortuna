from fastapi import APIRouter, Request
from starlette.responses import HTMLResponse, FileResponse
from starlette.authentication import requires
from fastapi.responses import RedirectResponse

from src.template import templates

router = APIRouter()


@router.get(
    path="/",
    response_class=HTMLResponse
)
@requires('authenticated', redirect='page_404')
async def index(request: Request):
    return RedirectResponse('/search/')


@router.get(
    path="/404",
    response_class=HTMLResponse
)
@requires('authenticated', redirect='login')
async def page_404(request: Request):
    return templates.TemplateResponse("/general_pages/global/404.html", 
                                      {"request": request})


@router.get('/favicon.ico', include_in_schema=False)
async def favicon():
    favicon_path = './src/static/icons/favicon.ico'
    return FileResponse(favicon_path)
