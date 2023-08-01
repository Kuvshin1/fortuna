import sys
from fastapi import APIRouter, Depends, HTTPException, Request
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.authentication import requires
from src.services.properties.properties_exceptions_http import properties_fail_http_resolver
from returns.pipeline import flow
from uuid import uuid4

from src.services.auth_logs import auth_log_service
from src.services.users.data.user_schema import UserRole, UserSchema

from src.services.users.users_router_web_schema import (AddUserTokenRequest,
                                                        DeprecateUserTokenRequest,
                                                        UpdateUserTokenRequest)
from src.services.users.data import users_repository
from src.services.tokens import token_repository
from src.services.tokens import token_service
from src.services.model.data import model_repository

from src.template import templates
from src.utils.fp.get_or_else_w import get_or_else_w

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get(
    path="/add",
    response_class=HTMLResponse
)
@requires(['authenticated', UserRole.ADMIN], redirect='page_404')
async def add_user_page(request: Request):
    models_list = model_repository.get_models(
        page=1,
        limit=sys.maxsize
    )
    return templates.TemplateResponse("/general_pages/settings/users/user-add.html", {"request": request, "models_list": models_list})


@router.get(
    path="/{id}",
    response_class=HTMLResponse
)
@requires(['authenticated', UserRole.ADMIN], redirect='page_404')
async def get_user_by_id_page(request: Request, id: str):
    user = users_repository.get_user_by_id(id)
    if user is None:
        return RedirectResponse('/404', status_code=303)
    tokens = token_repository.get_all_tokens_by_user_id(str(user.id))
    last_auth_log = auth_log_service.get_auth_logs(
        1, 1, {}, filtersAnd={'login': user.login})
    last_auth_log = last_auth_log[0] if last_auth_log else None
    return templates.TemplateResponse("/general_pages/settings/users/user-page.html",
                                      {"request": request,
                                        "user": user,
                                       "tokens": tokens,
                                       "last_auth_log": last_auth_log
                                       })


@router.get(
    path="/",
    response_class=HTMLResponse
)
@requires(['authenticated', UserRole.ADMIN], redirect='page_404')
async def user_list_page(request: Request, page: int = 1, limit: int = 10):
    users = list(map(lambda item: dict(item), users_repository.get_users(
        page=page,
        limit=limit
    )))
    for user in users:
        user.update(
            {"token": token_repository.get_token_by_user_id(user_id=str(user['id']))})
    users_count = len(users_repository.get_users(
        page=1,
        limit=sys.maxsize
    ))
    all_users_page_count = users_count // limit + \
        1 if users_count % limit else users_count // limit
    return templates.TemplateResponse(
        "/general_pages/settings/users/user-list.html",
        {"request": request, "users": users, 'current_page': page,
            'all_users_page_count': all_users_page_count}
    )


@router.post(
    path="/add",
    response_class=HTMLResponse
)
@requires(['authenticated', UserRole.ADMIN], redirect='page_404')
async def add_user_token(request: Request, add_user_form: AddUserTokenRequest = Depends(AddUserTokenRequest.as_form)):
    result = users_repository.add_user(
        login=add_user_form.login,
        role=add_user_form.role
    )

    try:
        user: UserSchema = flow(
            result,
            get_or_else_w(
                on_failure=properties_fail_http_resolver
            )
        )
    except HTTPException as ex:
        return templates.TemplateResponse("/general_pages/settings/users/user-add.html", {"request": request, 'error': ex.detail})

    token_value = uuid4()
    token_service.add_token(str(token_value), str(
        user.id), add_user_form.access_model_kinds)
    return templates.TemplateResponse("/general_pages/settings/users/user-add.html", {"request": request, 'token': str(token_value)})


@router.post(
    path="/{id}/deprecate",
    response_class=HTMLResponse
)
@requires(['authenticated', UserRole.ADMIN], redirect='page_404')
async def deprecate_user_token(
        request: Request,
        id: str,
        deprecate_user_form: DeprecateUserTokenRequest = Depends(
            DeprecateUserTokenRequest.as_form)
):
    token = token_repository.get_token_by_user_id(id)
    token_repository.update_token(
        token_id=str(token.id),
        update_token_filter={'deprecated': deprecate_user_form.deprecated}
    )
    return RedirectResponse(f"/settings/users/{id}", status_code=303)


@router.get(
    path="/{user_id}/update"
)
@requires(['authenticated', UserRole.ADMIN], redirect='page_404')
async def update_user_token_page(request: Request, user_id: str):
    models_list = model_repository.get_models(
        page=1,
        limit=sys.maxsize
    )
    user = users_repository.get_user_by_id(user_id)
    return templates.TemplateResponse("/general_pages/settings/users/user-update.html", {"request": request, "user": user, "models_list": models_list})


@router.post(
    path="/{user_id}/update"
)
@requires(['authenticated', UserRole.ADMIN], redirect='page_404')
async def update_user_token(request: Request, user_id: str, update_user_form: UpdateUserTokenRequest = Depends(UpdateUserTokenRequest.as_form)):
    user = users_repository.get_user_by_id(user_id)
    if user is None:
        return RedirectResponse('/404', status_code=303)

    last_token = token_repository.get_token_by_user_id(str(user.id))
    if last_token is not None:
        token_repository.update_token(
            token_id=str(last_token.id),
            update_token_filter={'deprecated': True}
        )

    token_value = uuid4()
    token_service.add_token(str(token_value), str(
        user_id), update_user_form.access_model_kinds)
    return templates.TemplateResponse("/general_pages/settings/users/user-update.html", {"request": request, "user": user, 'token': str(token_value)})
