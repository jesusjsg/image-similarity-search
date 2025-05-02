import io
import logging
from pathlib import Path
from typing import Annotated, Any, Dict, List

from fastapi import (APIRouter, Depends, File, HTTPException, Query, Request,
                     UploadFile, status)
from fastapi.concurrency import run_in_threadpool
from PIL import Image, UnidentifiedImageError

from app.core.config import settings
from app.core.dependencies import get_search_service
from app.schemas.image import SearchResponse
from app.services.image_search import ImageSearchService
from app.validators.upload_image_validator import validate_uploaded_image

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

#  Cambio del prefijo de la ruta a /search
router = APIRouter(prefix="/image", tags=["Image"])

#  Cambio de la ruta a /search/image


@router.post("/upload",
             summary="Upload an image",
             response_model=SearchResponse)
async def search_by_image(
    request: Request,
    service: Annotated[ImageSearchService, Depends(get_search_service)],
    file: UploadFile = File(..., description="Image file to upload"),
    top_k: Annotated[int, Query(
        gt=0, le=20, description="Number of top results to return")] = 20,
) -> SearchResponse:
    validate_contents = await validate_uploaded_image(file)
    try:
        query_image = Image.open(io.BytesIO(validate_contents))
    except UnidentifiedImageError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="El archivo no es una imagen válida."
        )
    finally:
        await file.close()

    results_paths, results_scores = await run_in_threadpool(
        service.search,
        query_image,
        top_k=top_k
    )

    response_items_list: List[Dict[str, Any]] = []
    base_url = str(settings.IMAGE_BASE_URL).strip("/")
    static_root = str(settings.STATIC_IMAGE_PATH.resolve())

    # refactor this for loop to use zip in other module
    for path, score in zip(results_paths, results_scores):
        url = None
        absolute_path = Path(path)
        filename_stem = absolute_path.stem
        try:
            relative_path = absolute_path.relative_to(static_root)
            url_path = "/".join(relative_path.parts)
            url = f"{base_url}/{url_path}"
        except Exception as e:
            log.error(f"Error creating URL for image: {e}")

        response_items_list.append({
            "name": filename_stem,
            "score": round(float(score), 2),
            "image_url": url
        })

    return SearchResponse(results=response_items_list)

#  Agregar la ruta para obtener la imagen por texto
