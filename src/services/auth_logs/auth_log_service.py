import sys
from typing import Any

from src.services.auth_logs.data import auth_logs_repository
from src.services.auth_logs.data.auth_log_schema import PasswordData
from src.utils.types.dict import filter_nullable_values_from_dict


def add_auth_log_success(login: str, password_id: str, ip: str, user_agent: str):
    return auth_logs_repository.add_auth_log(
        login=login,
        password=PasswordData(
            id=password_id
        ),
        ip=ip,
        user_agent=user_agent,
        success=True,
        reason=None
    )


def add_auth_log_failed(login: str, password: str, ip: str, user_agent: str, reason: str):
    return auth_logs_repository.add_auth_log(
        login=login,
        password=PasswordData(
            value=password
        ),
        ip=ip,
        user_agent=user_agent,
        success=False,
        reason=reason
    )


def get_auth_logs(page: int, limit: int, filtersOr: dict[str, Any], filtersAnd: dict[str, Any]):
    return auth_logs_repository.get_auth_logs(
        page,
        limit,
        filter_nullable_values_from_dict(filtersOr),
        filter_nullable_values_from_dict(filtersAnd)
    )


def get_count_auth_logs(filtersOr: dict[str, Any], filtersAnd: dict[str, Any]):
    return len(get_auth_logs(
        1,
        sys.maxsize,
        filtersOr,
        filtersAnd
    ))
