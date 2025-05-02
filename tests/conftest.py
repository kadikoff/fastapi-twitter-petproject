from io import BytesIO
from pathlib import Path

import pytest
from fastapi import UploadFile

from server.core.models import (
    Base,
    DatabaseHelper,
    Likes,
    Medias,
    Tweets,
    Users,
)

_BASE_TESTS_DIR = Path(__file__).parent
_MEDIAS_DIR = _BASE_TESTS_DIR / "data/medias"
_MEDIA_PATH = str(_BASE_TESTS_DIR / "data/medias/cat.jpeg")

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


@pytest.fixture(scope="session")
async def users_objs():
    return [
        Users(id=1, name="Nick Ivanov", api_key="test"),
        Users(id=2, name="Ivan Petrov", api_key="dev"),
    ]


@pytest.fixture(scope="session")
async def tweets_obj():
    return Tweets(tweet_id=1, tweet_data="Hello world!", user_id=1)


@pytest.fixture(scope="session")
async def medias_obj():
    return Medias(media_id=1, media_path=_MEDIA_PATH, tweet_id=1)


@pytest.fixture(scope="session")
async def likes_obj():
    return Likes(like_id=1, tweet_id=1, user_id=1)


@pytest.fixture(scope="session", autouse=True)
async def create_mock_data(
    global_db_session, users_objs, tweets_obj, medias_obj, likes_obj
):
    global_db_session.add_all(users_objs)
    await global_db_session.commit()

    global_db_session.add_all(
        (
            tweets_obj,
            medias_obj,
            likes_obj,
        )
    )
    await global_db_session.commit()


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
