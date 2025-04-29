from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.middleware.errors_handling_middleware import ErrorsHandlingMiddleware


def _setup_middleware(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=settings.ALLOW_CREDENTIALS,
        allow_methods=settings.ALLOWED_METHODS,
        allow_headers=settings.ALLOWED_HEADERS
    )
    app.add_middleware(ErrorsHandlingMiddleware)


def _setup_static_files(app: FastAPI) -> None:
    app.mount(
        "/static", StaticFiles(directory=settings.STATIC_IMAGE_PATH), name="static")


def setup_app(app: FastAPI) -> None:
    _setup_middleware(app)
    _setup_static_files(app)
