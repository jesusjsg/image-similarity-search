from fastapi import HTTPException, status

from app.core.config import settings
from app.core.logger import logger
from app.services.image_search import ImageSearchService

_search_service: ImageSearchService | None = None


def get_search_service() -> ImageSearchService:
    global _search_service
    if _search_service is None:
        try:
            _search_service = ImageSearchService(
                index_path=settings.INDEX_FAISS_PATH,
                mapping_path=settings.MAPPING_ROUTES_PATH,
                model_name=settings.CLIP_MODEL_NAME,
                device=settings.DEVICE
            )
        except Exception as e:
            logger.error(f"Error inicializando ImageSearchService: {e}")
            _search_service = None
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to initialize search service."
            )
    return _search_service
