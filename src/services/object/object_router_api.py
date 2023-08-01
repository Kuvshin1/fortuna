import codecs
import csv
import json
from datetime import datetime
from fastapi import APIRouter, BackgroundTasks, Request, Depends, UploadFile
from src.libs.auth_role.auth_role import role_required
from src.services.users.data.user_schema import UserRole
from src.types.pagination import ListResponse
from starlette.authentication import requires
from src.config import get_settings
from src.services.object.data.object_schema import ObjectStatus
from src.services.users.data import users_repository
from src.services.object.object_router_api_schema import (GetObjectsRequest, Object, ObjectDtResponse,
                                                        ObjectDt,
                                                        AddObjectRequest,
                                                        DeclineObjectRequest)
from src.services.object.data import object_repository
from src.services.object import object_service
from src.services.model.data import model_repository
from src.services.model import model_service


router = APIRouter(
    prefix="/objects",
    tags=["objects"],
)


@router.post(
    path="/add"
)
@requires('authenticated')
async def add_object(request: Request, add_object_form: AddObjectRequest = Depends(AddObjectRequest)):
    new_object = object_repository.add_object(
        owner_id=str(request.user.id),
        model_id=add_object_form.payload.model_id,
        payload=add_object_form.payload.properties
    )
    return new_object


@router.post(
    path="/list/dt",
    response_model=ObjectDtResponse
)
@requires('authenticated')
@role_required(UserRole.MODERATOR, UserRole.ADMIN)
async def get_objects_for_dt(request: Request):
    auth_user = request.user
    request = json.loads((await request.body()).decode("utf-8"))
    page = request['start'] // request['length'] + 1
    limit = request['length']
    search = request['search']['value'].strip()
    filtersOr = {column['data']: search
                 for column in request['columns']} if search else {}
    filtersAnd = request['filters']

    # Возвращаем только разрешенные модели
    available_models_list = model_service.get_available_models_by_user_id(auth_user)
    objects = object_service.get_objects_by_filter(
        page=page,
        limit=limit,
        filtersAnd=filtersAnd,
        model_ids=[str(schema.id)
                          for schema in available_models_list]
    )
    objectsDt = []
    for model in objects:
        if model.status.moderator_id != None:
            model.status.moderator_id = users_repository.get_user_by_id(
                str(model.status.moderator_id)).login

        model_name = model_repository.get_model_by_id(
            str(model.model_id)).name
        owner_id = users_repository.get_user_by_id(str(model.owner_id)).login
        objectDt = ObjectDt(id=model.id, created_at=model.created_at, status=model.status,
                          owner_id=owner_id,
                          model_id=str(model.model_id),
                          model_name=model_name)
        objectsDt.append(objectDt)

    count_objects = object_service.get_count_objects(
        filtersOr=filtersOr,
        filtersAnd=filtersAnd
    )
    return ObjectDtResponse(
        data=objectsDt,
        draw=request['draw'],
        recordsTotal=count_objects,
        recordsFiltered=count_objects
    )


@router.post(
    path="/several/approve",
)
@requires('authenticated')
@role_required(UserRole.MODERATOR, UserRole.ADMIN)
async def approveMany(request: Request, ids: list[str]):
    return object_service.change_status_objects('approve', ids, str(request.user.id))


@router.post(
    path="/several/decline",
)
@requires('authenticated')
@role_required(UserRole.MODERATOR, UserRole.ADMIN)
async def declineMany(request: Request, ids: list[str]):
    return object_service.change_status_objects('decline', ids, str(request.user.id))


@router.post(
    path="/all/decline",
)
@requires('authenticated')
@role_required(UserRole.MODERATOR, UserRole.ADMIN)
async def declineAll(request: Request, filters: dict):
    ids = object_service.get_objects_ids_by_filters(filters)
    return object_service.change_status_objects('decline', ids, str(request.user.id))


@router.post(
    path="/all/approve",
)
@requires('authenticated')
@role_required(UserRole.MODERATOR, UserRole.ADMIN)
async def approveAll(request: Request, filters: dict):
    ids = object_service.get_objects_ids_by_filters(filters)
    return object_service.change_status_objects('approve', ids, str(request.user.id))


@router.post(
    path="/file/upload"
)
@requires('authenticated')
async def upload_file(request: Request, background_tasks: BackgroundTasks, file: UploadFile):
    csv_reader = csv.DictReader(codecs.iterdecode(
        file.file, get_settings().encoding_models_file))
    background_tasks.add_task(file.file.close)
    list_csv_reader = list(csv_reader)
    try:
        model_id = str(model_repository.get_actual_model_by_name(
            list(list_csv_reader[0].keys())[1].split('|')[0]).id)
        list_models_payloads = object_service.csv_to_objects_parser(list_csv_reader)
    except:
        return False
    return object_repository.add_many_objects(request.user.id, model_id, list_models_payloads)


@router.post(
    path="/{id}/approve"
)
@requires('authenticated')
@role_required(UserRole.MODERATOR, UserRole.ADMIN)
async def approve_object(request: Request, id: str):
    status = ObjectStatus(approve_at=datetime.utcnow(),
                         moderator_id=str(request.user.id))
    return object_repository.update_object(id, status)


@router.post(
    path="/{id}/decline"
)
@requires('authenticated')
@role_required(UserRole.MODERATOR, UserRole.ADMIN)
async def decline_object(request: Request, decline_form: DeclineObjectRequest):
    status = ObjectStatus(decline_at=datetime.utcnow(), moderator_id=str(
        request.user.id), reason=decline_form.reason)
    return object_repository.update_object(decline_form.id, status)


@router.post(
    path="/"
)
@requires('authenticated')
async def get_objects(request: Request, get_objects_request: GetObjectsRequest) -> ListResponse[Object]:
    available_models_list = model_service.get_available_models_by_user_id(
        request.user)
    filtersAnd = {
        'status': 'approved'
    }
    objects = object_service.get_objects_by_filter(
        page=get_objects_request.page,
        limit=get_objects_request.count,
        filtersAnd=filtersAnd,
        model_ids=[str(schema.id)
                          for schema in available_models_list],
        text=get_objects_request.text
    )
    return ListResponse(
        count=len(objects),
        page_number=get_objects_request.page,
        is_next=len(objects) == get_objects_request.count,
        data=objects
    )
