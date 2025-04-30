import random
from datetime import datetime
from pathlib import Path

import aiofiles
from fastapi import HTTPException, UploadFile, status

from server.core.config import BASE_MEDIAS_DIR, MEDIAS_ALLOWED_EXT


async def validate_media(file_name: str) -> None:
    file_ext = Path(file_name).suffix.lower()
    if file_ext not in MEDIAS_ALLOWED_EXT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file format! Acceptable: "
            f"{', '.join(MEDIAS_ALLOWED_EXT)}",
        )


async def generate_media_file_name(file_name: str) -> str:
    file_ext = Path(file_name).suffix.lower()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    random_num = random.randint(1, 10_000)

    return f"{timestamp}_{random_num}{file_ext}"


async def save_media(file: UploadFile):
    await validate_media(file_name=file.filename)
    new_file_name: str = await generate_media_file_name(
        file_name=file.filename
    )

    file_path = BASE_MEDIAS_DIR / new_file_name

    try:
        file_bytes = await file.read()
        async with aiofiles.open(file_path, mode="wb") as media_file:
            await media_file.write(file_bytes)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error while saving a media file: {exc}",
        )

    return file_path


async def delete_media(file_path: Path) -> None:
    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File not found: {file_path}",
        )

    try:
        file_path.unlink()
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error while deletion a media file: {exc}",
        )
