import io
from typing import Annotated, List, Dict, Any
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, status, Request, Query
from fastapi.concurrency import run_in_threadpool
from PIL import Image
from pathlib import Path
from app.services.image_search import ImageSearchService
from app.core.config import settings
from app.core.dependencies import get_search_service
from app.schemas.image import SearchResponse


router = APIRouter(prefix="/image", tags=["Image"])


@router.post("/upload",
             summary="Upload an image",
             response_model=SearchResponse)
async def upload_image(
    request: Request,
    service: Annotated[ImageSearchService, Depends(get_search_service)],
    file: UploadFile = File(..., description="Image file to upload"),
    top_k: Annotated[int, Query(
        gt=0, le=20, description="Number of top results to return")] = 20,
) -> SearchResponse:
    try:
        contents = await file.read()
        query_image = Image.open(io.BytesIO(contents))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing image: {str(e)}"
        )
    finally:
        await file.close()

    try:
        results_paths, results_scores = await run_in_threadpool(
            service.search, query_image, top_k
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error searching for similar images: {str(e)}"
        )

    response_items_list = List[Dict[str, Any]] = []
    base_url = str(settings.IMAGE_BASE_URL).strip("/")
    static_root = str(settings.STATIC_IMAGE_PATH.resolve())

    for path, score in zip(results_paths, results_scores):
        url = None
        absolute_path = Path(path)
        filename_stem = absolute_path.stem
        try:
            relative_path = absolute_path.relative_to(static_root)
            url_path = "/".join(relative_path.parts)
            url = f"{base_url}/{url_path}"
        except Exception as e:
            print(f"Error processing path {path}: {e}")

        response_items_list.append({
            "name": filename_stem,
            "score": float(score),
            "image_url": url
        })

    return {
        "results": response_items_list,
    }
