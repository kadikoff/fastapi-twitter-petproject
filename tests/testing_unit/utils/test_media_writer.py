import pytest
from fastapi import HTTPException

from server.utils.media_writer import (
    create_medias_directory,
    save_media,
    delete_media,
    validate_media,
)


@pytest.mark.asyncio
async def test_create_medias_directory_success(path_to_medias_dir):
    await create_medias_directory(path=path_to_medias_dir)
    assert path_to_medias_dir.exists()


@pytest.mark.asyncio
async def test_save_and_delete_media_success(sample_media_jpg, path_to_medias_dir):
    file_path = await save_media(file=sample_media_jpg, path_to_save=path_to_medias_dir)
    assert file_path.exists()
    assert file_path.parent == path_to_medias_dir
    assert file_path.suffix == ".jpg"

    await delete_media(file_path=file_path)
    assert not file_path.exists()


@pytest.mark.asyncio
async def test_save_media_not_exist_dir(sample_media_jpg, path_to_medias_dir):
    fake_path_to_medias_dir = path_to_medias_dir / "fake_dir"

    with pytest.raises(HTTPException) as exc_info:
        await save_media(file=sample_media_jpg, path_to_save=fake_path_to_medias_dir)

    assert exc_info.value.status_code == 500


@pytest.mark.asyncio
async def test_validate_media_not_allowed_ext(sample_media_pdf):
    file_name = sample_media_pdf.filename

    with pytest.raises(HTTPException) as exc_info:
        await validate_media(file_name=file_name)

    assert exc_info.value.status_code == 400
