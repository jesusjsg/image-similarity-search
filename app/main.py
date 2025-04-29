import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers import images as images_router
from app.services.image_search import ImageSearchService
from app.core.config import settings
from app.core.app_setup import setup_app

os.environ["KMP_DUPLICATE_LIB_OK"] = "True"


@asynccontextmanager
async def lifespan(app: FastAPI):
    service_instance = None
    try:
        service_instance = ImageSearchService(
            index_path=settings.INDEX_FAISS_PATH,
            mapping_path=settings.MAPPING_ROUTES_PATH,
            model_name=settings.CLIP_MODEL_NAME,
            device=settings.DEVICE
        )
        print("ImageSearchService initialized successfully.")
        app.state.search_service = service_instance
    except FileNotFoundError as e:
        print(f"Error initializing ImageSearchService: {e}")
        app.state.search_service = service_instance
    except Exception as e:
        print(f"Unexpected error initializing ImageSearchService: {e}")
        app.state.search_service = service_instance
    yield  # Inicio de la aplicación

app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

setup_app(app)

app.include_router(images_router.router, tags=["Images-search"])
