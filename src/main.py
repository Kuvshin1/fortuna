import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.constants import MODELS_TEMPLATES_FOLDER, TEMP_FOLDER_RELATIVE_PATH
from starlette.staticfiles import StaticFiles
from starlette.middleware.authentication import AuthenticationMiddleware
from src.config import get_settings
from src.database.initiate_database import initiate_database
from src.middlewaries.web_auth_middleware import AuthMiddleware

from src.services.authentication import (authentication_router_api, 
                                         authentication_router_web)
from src.services.model import (model_router_api, 
                                         model_router_web)
from src.services.properties import (properties_router_api, 
                                     properties_router_web)
from src.services.auth_logs import (auth_log_router_api, 
                                    auth_log_router_web)
from src.services.object import object_router_api, object_router_web
from src.routers import search_router_web
from src.routers import root_router_web
from src.routers import user_guide_router_web
from src.services.users import users_router_web
from src.utils.relative_path import from_module_path_to
from src.exceptions_handler import exception_handlers

settings = get_settings()


def init_db(_app: FastAPI):
    @_app.on_event("startup")
    def startup_db_client():
        app.mongodb_client = initiate_database()

    @_app.on_event("shutdown")
    def shutdown_db_client():
        app.mongodb_client.close()

def init_middlewaries(app: FastAPI):
    app.add_middleware(
        AuthenticationMiddleware, 
        backend=AuthMiddleware()
    )


def init_web_routers(app: FastAPI):
    app.include_router(auth_log_router_web.router)
    app.include_router(authentication_router_web.router)
    app.include_router(object_router_web.router)
    app.include_router(root_router_web.router)
    app.include_router(search_router_web.router)
    app.include_router(user_guide_router_web.router)
    app.include_router(properties_router_web.router, prefix='/settings')
    app.include_router(users_router_web.router, prefix='/settings')
    app.include_router(model_router_web.router, prefix='/settings')

def init_api_routers(app: FastAPI):
    app.include_router(auth_log_router_api.router, prefix=settings.api_prefix)
    app.include_router(authentication_router_api.router, 
                       prefix=settings.api_prefix)
    app.include_router(model_router_api.router, 
                       prefix=settings.api_prefix)
    app.include_router(object_router_api.router, prefix=settings.api_prefix)
    app.include_router(properties_router_api.router, 
                       prefix=settings.api_prefix)

def init_cors(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

def init_static_folders(_app: FastAPI):
    _app.mount(
        "/static",
        StaticFiles(directory=from_module_path_to("static")),
        name="static"
    )

def init_folders():
    folders = [
        os.path.join(TEMP_FOLDER_RELATIVE_PATH, MODELS_TEMPLATES_FOLDER)
    ]
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)

def init_app() -> FastAPI:
    app = FastAPI(
        exception_handlers=exception_handlers
    )
    init_folders()
    init_middlewaries(app)
    init_web_routers(app)
    init_api_routers(app)
    init_db(app)
    init_static_folders(app)
    return app


app = init_app()
