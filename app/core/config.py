from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str
    INDEX_FAISS_PATH: Path
    MAPPING_ROUTES_PATH: Path
    CLIP_MODEL_NAME: str
    DEVICE: str
    STATIC_IMAGE_PATH: Path
    IMAGE_BASE_URL: str
    MAX_UPLOAD_SIZE: int
    ALLOWED_ORIGINS: list[str] = ["*"]
    ALLOWED_METHODS: list[str] = ["GET", "POST", "PUT", "DELETE"]
    ALLOWED_HEADERS: list[str] = ["*"]
    ALLOW_CREDENTIALS: bool

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = "APP_"


settings = Settings()
