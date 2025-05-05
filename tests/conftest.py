from io import BytesIO

import pytest
from fastapi import UploadFile
from httpx import ASGITransport, AsyncClient
from sqlalchemy import insert

from server.core.models import (
    Base,
    DatabaseHelper,
    Medias,
    Tweets,
    Users,
    db_helper,
)
from server.main import app
from tests.data.data_db_mock import (
    MEDIAS_DIR,
    medias_correct,
    tweets_correct,
    users_correct,
)

_db_helper = DatabaseHelper(
    url="sqlite+aiosqlite:///./tests/data/test.db", echo=True
)


@pytest.fixture(scope="session")
async def create_db():
    async with _db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture
async def db_session(create_db):
    async with _db_helper.session_factory() as session:
        yield session
        await session.close()


@pytest.fixture(scope="session")
async def global_db_session(create_db):
    """
    Сессия для session-scoped фикстур

    Создана дополнительная фикстура для получения сессии (именно для фикстуры
    create_mock_data), т.к. возникает ошибка ScopeMismatch из-за несоответствия
    областей видимости при вызове фикстуры db_session со scope="function"
    из фикстуры create_mock_data со scope="session" и autouse=True
    """
    async with _db_helper.session_factory() as session:
        yield session
        await session.close()


@pytest.fixture
async def client(db_session):
    """Создание тестового клиента и переопределение сессии"""

    async def override_get_db():
        yield db_session

    app.dependency_overrides[db_helper.session_dependency] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture(scope="session", autouse=True)
async def create_mock_data(global_db_session):
    await global_db_session.execute(insert(Users), users_correct)
    await global_db_session.execute(insert(Tweets), tweets_correct)
    await global_db_session.execute(insert(Medias), medias_correct)
    await global_db_session.commit()


@pytest.fixture(scope="session", autouse=True)
async def create_test_medias_dir():
    MEDIAS_DIR.mkdir(mode=0o755, parents=True, exist_ok=True)


@pytest.fixture
async def path_to_medias_dir():
    return MEDIAS_DIR


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
