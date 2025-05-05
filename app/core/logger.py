import logging

from app.core.config import settings


def setup_logging():
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
        format=settings.LOG_FORMAT,
    )
    logger = logging.getLogger(__name__)
    return logger


logger = setup_logging()
