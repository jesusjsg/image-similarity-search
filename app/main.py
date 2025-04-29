import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from app.routers import images as images_router
from app.core.config import settings
from app.services.image_search import ImageSearchService
from app.middleware.errors_handling_middleware import ErrorsHandlingMiddleware

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
    except Exception as e:
        print(f"Error initializing ImageSearchService: {e}")
    app.state.search_service = service_instance
    yield
    app.state.search_service = None

app = FastAPI(title="Image Search API", lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.add_middleware(ErrorsHandlingMiddleware)

app.include_router(images_router.router, tags=["Images-search"])

if settings.STATIC_IMAGE_PATH.exists() and settings.STATIC_IMAGE_PATH.is_dir():
    app.mount(
        "/static",
        StaticFiles(directory=settings.STATIC_IMAGE_PATH),
        name="static"
    )
    print(f"Mounted static files from {settings.STATIC_IMAGE_PATH}")
