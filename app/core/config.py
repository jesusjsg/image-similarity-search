from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    INDEX_FAISS_PATH: Path
    MAPPING_ROUTES_PATH: Path
    CLIP_MODEL_NAME: str
    DEVICE: str
    STATIC_IMAGE_PATH: Path
    IMAGE_BASE_URL: str
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10 MB

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = "APP_"


settings = Settings()
