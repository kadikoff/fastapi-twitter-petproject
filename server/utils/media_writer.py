import aiofiles
from fastapi import UploadFile

from server.core.config import BASE_MEDIAS_DIR


async def save_media(file: UploadFile):

    file_name = file.filename
    file_path = BASE_MEDIAS_DIR / file_name
    file_bytes = file.file.read()
    async with aiofiles.open(file_path, mode="wb") as media_file:
        await media_file.write(file_bytes)

    return file_path
