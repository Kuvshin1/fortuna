from fastapi import APIRouter, Depends, HTTPException, Request, status
from returns.pipeline import flow
from starlette.responses import HTMLResponse
from src.services.authentication import authentication_service
from src.services.authentication.authentication_router_web_schema import LoginForm
from src.services.authentication.authentication_exceptions_http import auth_fail_http_resolver
from starlette.responses import RedirectResponse
from src.services.authentication.authentication_service_model import TokenModel, ClientInformation

from src.template import templates
from src.utils.fp.get_or_else_w import get_or_else_w


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.get(
    path="/login",
    response_class=HTMLResponse
)
async def login_page(request: Request):
    return templates.TemplateResponse("/general_pages/login/login.html", {"request": request})


@router.post(
    path="/login"
)
async def login(request: Request, login_form: LoginForm = Depends(LoginForm.as_form)):
    result = authentication_service.login(login_form, ClientInformation(
        ip=f"{request.client.host}:{request.client.port}",
        user_agent=request.headers['User-Agent']
    ))

    try:
        token_response: TokenModel = flow(
            result,
            get_or_else_w(
                on_failure=auth_fail_http_resolver
            )
        )
    except HTTPException as ex:
        return templates.TemplateResponse("/general_pages/login/login.html", {"request": request, 'error': ex.detail})

    response = RedirectResponse(url='/', status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(
        "Authorization",
        value=f"{token_response.token_type} {token_response.access_token}",
        max_age=1800,
        expires=1800,
    )
    return response


@router.get("/logout")
async def route_logout_and_remove_cookie():
    response = RedirectResponse(url="/auth/login")
    response.delete_cookie("Authorization")
    return response
