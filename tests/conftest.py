from io import BytesIO
from pathlib import Path

import pytest
from fastapi import UploadFile

from server.core.models import (
    DatabaseHelper,
    Base,
)

_BASE_TESTS_DIR = Path(__file__).parent
_MEDIAS_DIR = _BASE_TESTS_DIR / "data/medias"

_db_helper = DatabaseHelper(
    url="sqlite+aiosqlite:///./tests/data/test.db",
    echo=True
)


@pytest.fixture(scope="session", autouse=True)
async def create_db():
    async with _db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture
async def db_session():
    async with _db_helper.session_factory() as session:
        yield session
        await session.close()


@pytest.fixture(scope="session", autouse=True)
async def create_test_medias_dir():
    _MEDIAS_DIR.mkdir(mode=0o755, parents=True, exist_ok=True)


@pytest.fixture
async def path_to_medias_dir():
    return _MEDIAS_DIR


@pytest.fixture
async def sample_media_jpg():
    content = b"fake media"
    file_name = "test.jpg"
    return UploadFile(filename=file_name, file=BytesIO(content))


@pytest.fixture
async def sample_media_pdf():
    content = b"fake media"
    file_name = "test.pdf"
    return UploadFile(filename=file_name, file=BytesIO(content))

