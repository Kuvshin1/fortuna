import sys

from src.services.users.data import users_repository


def get_all_users():
    return users_repository.get_users(1, sys.maxsize)


def get_user_by_id(id: str):
    return users_repository.get_user_by_id(id)
