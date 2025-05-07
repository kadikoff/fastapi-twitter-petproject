import pytest
from fastapi import HTTPException
from sqlalchemy import Result, select

from server.api.crud import crud_users
from server.core.models import Users
from server.core.models import followers_association_table as fat
from server.utils.hashed_api_key import validate_api_key
from tests.data.data_db_mock import users_correct


@pytest.mark.asyncio
async def test_get_user_by_api_key_success(db_session):
    """Тест успешного получения пользователя по api_key"""

    user_data: dict = users_correct[0]

    user: Users | None = await crud_users.get_user_by_api_key(
        session=db_session, api_key=user_data["api_key"]
    )

    assert user is not None
    assert isinstance(user, Users)
    assert user.name == user_data["name"]
    assert validate_api_key(
        api_key=user_data["api_key"], hashed_api_key=user.api_key
    )


@pytest.mark.asyncio
async def test_get_user_by_api_key_error(db_session):
    """Тест обработки ошибки при получении пользователя
    по api_key с использованием не существующего api_key
    """

    fake_api_key = "fake_api_key"

    with pytest.raises(HTTPException) as exc_info:
        await crud_users.get_user_by_api_key(
            session=db_session, api_key=fake_api_key
        )

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "API Key Authentication failed!"


@pytest.mark.asyncio
async def test_get_user_by_id_success(db_session):
    """Тест успешного получения пользователя по его id"""

    user_data: dict = users_correct[0]

    user: Users | None = await crud_users.get_user_by_id(
        session=db_session, user_id=user_data["id"]
    )

    assert user is not None
    assert isinstance(user, Users)
    assert user.name == user_data["name"]
    assert validate_api_key(
        api_key=user_data["api_key"], hashed_api_key=user.api_key
    )


@pytest.mark.asyncio
async def test_get_user_by_id_error(db_session):
    """Тест обработки ошибки при получении
    пользователя по не существующему id
    """

    fake_user_id = 123456789

    with pytest.raises(HTTPException) as exc_info:
        await crud_users.get_user_by_id(
            session=db_session, user_id=fake_user_id
        )

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == f"User '{fake_user_id}' not found!"


@pytest.mark.asyncio
async def test_create_follow_success(db_session):
    """Тест успешного создания подписки одного
    пользователя на другого
    """

    user_data_1 = Users(**users_correct[0])
    user_id_1: int = user_data_1.id
    user_data_2: dict = users_correct[1]
    user_id_2: int = user_data_2["id"]

    await crud_users.create_follow(
        session=db_session, current_user=user_data_1, user_id=user_id_2
    )

    stmt = select(fat).where(
        fat.c.follower_id == user_id_1, fat.c.following_id == user_id_2
    )
    db_response: Result = await db_session.execute(stmt)
    followers: fat | None = db_response.scalar_one_or_none()

    assert followers is not None


@pytest.mark.asyncio
async def test_create_follow_error(db_session):
    """Тест обработки ошибки при создании
    подписки одного пользователя на несуществующего
    """

    user_data = Users(**users_correct[0])
    user_id_1: int = user_data.id
    fake_user_id_2 = 123456789

    with pytest.raises(HTTPException) as exc_info:
        await crud_users.create_follow(
            session=db_session, current_user=user_data, user_id=fake_user_id_2
        )

    stmt = select(fat).where(
        fat.c.follower_id == user_id_1, fat.c.following_id == fake_user_id_2
    )
    db_response: Result = await db_session.execute(stmt)
    followers: fat | None = db_response.scalar_one_or_none()

    assert followers is None
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == f"User '{fake_user_id_2}' not found!"


@pytest.mark.asyncio
async def test_delete_follow_success(db_session):
    """Тест успешного удаления подписки одного
    пользователя на другого
    """

    user_data_1 = Users(**users_correct[0])
    user_id_1: int = user_data_1.id
    user_data_2: dict = users_correct[1]
    user_id_2: int = user_data_2["id"]

    await crud_users.delete_follow(
        session=db_session, current_user=user_data_1, user_id=user_id_2
    )

    stmt = select(fat).where(
        fat.c.follower_id == user_id_1, fat.c.following_id == user_id_2
    )
    db_response: Result = await db_session.execute(stmt)
    followers: fat | None = db_response.scalar_one_or_none()

    assert followers is None
