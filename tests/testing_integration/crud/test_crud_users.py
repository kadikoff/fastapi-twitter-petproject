import pytest
from fastapi import HTTPException

from server.api.crud import crud_users
from server.core.models import Users


@pytest.mark.asyncio
async def test_get_user_by_api_key_correct(db_session, users_objs):
    user_obj = users_objs[0]
    user = await crud_users.get_user_by_api_key(
        session=db_session, api_key=user_obj.api_key
    )

    assert user
    assert isinstance(user, Users)
    assert user.name == user_obj.name
    assert user.api_key == user_obj.api_key


@pytest.mark.asyncio
async def test_get_user_by_api_key_error(db_session):
    fake_api_key = "fake_api_key"

    with pytest.raises(HTTPException) as exc_info:
        await crud_users.get_user_by_api_key(
            session=db_session, api_key=fake_api_key
        )

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "API Key Authentication failed!"


@pytest.mark.asyncio
async def test_get_user_by_id_correct(db_session, users_objs):
    user_obj = users_objs[0]
    user = await crud_users.get_user_by_id(
        session=db_session, user_id=user_obj.id
    )

    assert user
    assert isinstance(user, Users)
    assert user.name == user_obj.name
    assert user.api_key == user_obj.api_key


@pytest.mark.asyncio
async def test_get_user_by_id_error(db_session):
    fake_user_id = 123456789

    with pytest.raises(HTTPException) as exc_info:
        await crud_users.get_user_by_id(
            session=db_session, user_id=fake_user_id
        )

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == f"User '{fake_user_id}' not found!"


@pytest.mark.asyncio
async def test_create_follow_correct(db_session, users_objs):
    user_obj_1 = users_objs[0]
    user_obj_2 = users_objs[1]

    await crud_users.create_follow(
        session=db_session, current_user=user_obj_1, user_id=user_obj_2.id
    )


@pytest.mark.asyncio
async def test_create_follow_error(db_session, users_objs):
    user_obj = users_objs[0]
    fake_user_id = 123456789

    with pytest.raises(HTTPException) as exc_info:
        await crud_users.create_follow(
            session=db_session, current_user=user_obj, user_id=fake_user_id
        )

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == f"User '{fake_user_id}' not found!"


@pytest.mark.asyncio
async def test_delete_follow_correct(db_session, users_objs):
    user_obj_1 = users_objs[0]
    user_obj_2 = users_objs[1]

    await crud_users.delete_follow(
        session=db_session, current_user=user_obj_1, user_id=user_obj_2.id
    )
