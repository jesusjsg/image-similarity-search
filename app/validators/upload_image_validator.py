from fastapi import UploadFile, HTTPException, status
from typing import Set, Optional
from app.core.config import settings

ALLOWED_IMAGE_MIME_TYPES: Set[str] = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/gif"
}

MAX_BYTES = settings.MAX_UPLOAD_SIZE


async def validate_uploaded_image(file: UploadFile) -> bytes:
    if not file.content_type:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="File content type is missing."
        )

    if file.content_type not in ALLOWED_IMAGE_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid file type."
        )

    contents: Optional[bytes] = None
    try:
        contents = await file.read()
        if len(contents) > MAX_BYTES:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"File size exceeds the limit of {MAX_BYTES / 1024 / 1024} MB."
            )
        return contents
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Error reading file: {str(e)}"
        )
    finally:
        await file.close()
