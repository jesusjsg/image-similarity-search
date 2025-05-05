from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # FastAPI settings
    PROJECT_NAME: str
    INDEX_FAISS_PATH: Path
    MAPPING_ROUTES_PATH: Path
    CLIP_MODEL_NAME: str
    DEVICE: str
    STATIC_IMAGE_PATH: Path
    IMAGE_BASE_URL: str
    MAX_UPLOAD_SIZE: int

    # CORS settings
    ALLOWED_ORIGINS: list[str] = ["*"]
    ALLOWED_METHODS: list[str] = ["GET", "POST", "PUT", "DELETE"]
    ALLOWED_HEADERS: list[str] = ["Content-Type", "Authorization"]
    ALLOW_CREDENTIALS: bool

    # Log settings
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = "APP_"


settings = Settings()
