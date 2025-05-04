from pathlib import Path

import pytest
from fastapi import HTTPException

from server.utils.media_writer import (
    create_medias_directory,
    delete_media,
    save_media,
    validate_media,
)


@pytest.mark.asyncio
async def test_create_medias_directory_success(path_to_medias_dir):
    """Тест успешного создания директории для хранения медиа"""

    await create_medias_directory(path=path_to_medias_dir)
    assert path_to_medias_dir.exists()


@pytest.mark.asyncio
async def test_save_and_delete_media_success(
    sample_media_jpg, path_to_medias_dir
):
    """Тест успешного сохранения и удаления медиа"""

    file_path: Path | None = await save_media(
        file=sample_media_jpg, path_to_save=path_to_medias_dir
    )
    assert file_path.exists()
    assert file_path.parent == path_to_medias_dir
    assert file_path.suffix == ".jpg"

    await delete_media(file_path=file_path)
    assert not file_path.exists()


@pytest.mark.asyncio
async def test_validate_media_not_allowed_ext(sample_media_pdf):
    """Тест обработки ошибки при создании медиа
    с неподдерживаемым расширением файла
    """

    file_name: str = sample_media_pdf.filename

    with pytest.raises(HTTPException) as exc_info:
        await validate_media(file_name=file_name)

    assert exc_info.value.status_code == 400
