from fastapi import APIRouter, Request
from starlette.responses import HTMLResponse
from starlette.authentication import requires
from src.template import templates

router = APIRouter(
    prefix="/user_guide",
    tags=["user_guide"],
)


@router.get(
    path="/",
    response_class=HTMLResponse
)
@requires('authenticated', redirect='login')
async def user_guide_page(request: Request):
    return templates.TemplateResponse(
        "/general_pages/user_guide/user-guide.html",
        {
            'request': request,
        }
    )
