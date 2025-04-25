from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    INDEX_FAISS_PATH: Path
    MAPPING_ROUTES_PATH: Path
    CLIP_MODEL_NAME: str
    DEVICE: str
    STATIC_IMAGE_PATH: Path
    IMAGE_BASE_URL: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
