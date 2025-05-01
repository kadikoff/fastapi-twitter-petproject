from io import BytesIO
from pathlib import Path

import pytest
from fastapi import UploadFile

_TEST_MEDIA_DIR = Path(__file__).parent.parent / "tests_utils/medias"


@pytest.fixture
def medias_folder_path():
    return _TEST_MEDIA_DIR


@pytest.fixture
def sample_media_jpg():
    content = b"fake media"
    file_name = "test.jpg"
    return UploadFile(filename=file_name, file=BytesIO(content))


@pytest.fixture
def sample_media_pdf():
    content = b"fake media"
    file_name = "test.pdf"
    return UploadFile(filename=file_name, file=BytesIO(content))