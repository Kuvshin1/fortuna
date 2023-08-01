from fastapi import APIRouter, Request
from src.services.users.data.user_schema import UserRole
from starlette.responses import HTMLResponse
from starlette.authentication import requires

from src.services.users import users_service
from src.template import templates

router = APIRouter(
    prefix="/auth_logs",
    tags=["auth_logs"],
)


@router.get(
    path="/",
    response_class=HTMLResponse
)
@requires(['authenticated', UserRole.ADMIN], redirect='page_404')
async def auth_logs_page(request: Request, 
                         success: bool | None = None, 
                         user: str | None = None):
    users = users_service.get_all_users()
    return templates.TemplateResponse(
        "/general_pages/logs/auth-logs-list.html",
        {"request": request, "users": users, 
         "success": success, "login": user}
    )
