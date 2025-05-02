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

print(f"Settings loaded: {settings.PROJECT_NAME}")
print(f"Index FAISS Path: {settings.INDEX_FAISS_PATH}")
print(f"Mapping Routes Path: {settings.MAPPING_ROUTES_PATH}")
print(f"CLIP Model Name: {settings.CLIP_MODEL_NAME}")
print(f"Device: {settings.DEVICE}")
print(f"Static Image Path: {settings.STATIC_IMAGE_PATH}")
print(f"Image Base URL: {settings.IMAGE_BASE_URL}")
print(f"Max Upload Size: {settings.MAX_UPLOAD_SIZE}")
print(f"Allowed Origins: {settings.ALLOWED_ORIGINS}")
print(f"Allowed Methods: {settings.ALLOWED_METHODS}")
print(f"Allowed Headers: {settings.ALLOWED_HEADERS}")
print(f"Allow Credentials: {settings.ALLOW_CREDENTIALS}")
print(f"Settings loaded successfully.")
