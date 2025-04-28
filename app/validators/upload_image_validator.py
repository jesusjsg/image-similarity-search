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
            detail="El archivo no se ha subido correctamente."
        )

    if file.content_type not in ALLOWED_IMAGE_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"El tipo de archivo no es válido."
        )

    contents: Optional[bytes] = None
    try:
        contents = await file.read()
        if len(contents) > MAX_BYTES:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"El tamaño del archivo es demasiado grande."
            )
        return contents
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Error al leer el archivo."
        )
    finally:
        await file.close()
