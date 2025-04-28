from fastapi import UploadFile, HTTPException, status
from typing import Set

ALLOWED_IMAGE_EXTENSIONS: Set[str] = {
    "image/jpeg",
    "image/jpg",
    "image/png",
    "image/webp",
    "image/gif"
}


def validate_file_content_type(file: UploadFile):
    if not file.content_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File content type is missing."
        )

    if file.content_type not in ALLOWED_IMAGE_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file type."
        )
