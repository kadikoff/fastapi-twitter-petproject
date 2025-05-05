import pytest
from sqlalchemy import Result, select

from server.core.models import followers_association_table as fat
from tests.data.data_db_mock import users_correct


@pytest.mark.asyncio
async def test_users_me_success(client):
    """Тест успешного запроса к API
    GET /api/users/me
    """

    response = await client.get("/api/users/me", headers={"api-key": "test"})
    data = response.json()

    assert response.status_code == 200
    assert data["result"] is True
    assert data["user"]
    assert data["user"]["id"]


@pytest.mark.asyncio
async def test_users_me_error(client):
    """Тест обработки ошибки при запросе к API
    GET /api/users/me с использованием
    несуществующего api_key
    """

    response = await client.get(
        "/api/users/me", headers={"api-key": "fake_api_key"}
    )
    data = response.json()

    assert response.status_code == 401
    assert data["result"] is False
    assert data["error_type"] == 401
    assert data["error_message"] == "API Key Authentication failed!"


@pytest.mark.asyncio
async def test_get_user_success(client):
    """Тест успешного запроса к API
    GET /api/users/{user_id}
    """

    user_id = users_correct[0]["id"]

    response = await client.get(f"/api/users/{user_id}")
    data = response.json()

    assert response.status_code == 200
    assert data["result"] is True
    assert data["user"]
    assert data["user"]["id"] == user_id


@pytest.mark.asyncio
async def test_get_user_error(client):
    """Тест обработки ошибки при запросе к API
    GET /api/users/{user_id} с использованием
    user_id несуществующего пользователя
    """

    fake_user_id = 123456789
    response = await client.get(f"/api/users/{fake_user_id}")
    data = response.json()

    assert response.status_code == 404
    assert data["result"] is False
    assert data["error_type"] == 404
    assert data["error_message"] == f"User '{fake_user_id}' not found!"


@pytest.mark.asyncio
async def test_create_follow_success(client, db_session):
    """Тест успешного запроса к API
    POST /api/users/{user_id}/follow
    """

    user_id_1 = users_correct[0]["id"]
    user_api_key_1 = users_correct[0]["api_key"]
    user_id_2 = users_correct[1]["id"]

    response = await client.post(
        f"/api/users/{user_id_2}/follow",
        headers={"api-key": user_api_key_1},
    )
    data = response.json()

    assert response.status_code == 200
    assert data["result"] is True

    stmt = select(fat).where(
        fat.c.follower_id == user_id_1, fat.c.following_id == user_id_2
    )
    db_response: Result = await db_session.execute(stmt)
    followers: fat | None = db_response.scalar_one_or_none()

    assert followers is not None


@pytest.mark.asyncio
async def test_create_follow_error(client, db_session):
    """Тест обработки ошибки при запросе к API
    POST /api/users/{user_id}/follow с использованием
    user_id несуществующего пользователя
    """

    user_api_key_1 = users_correct[0]["api_key"]
    user_id_1 = users_correct[0]["id"]
    fake_user_id_2 = 123456789

    response = await client.post(
        f"/api/users/{fake_user_id_2}/follow",
        headers={"api-key": user_api_key_1},
    )
    data = response.json()

    assert response.status_code == 404
    assert data["result"] is False
    assert data["error_type"] == 404
    assert data["error_message"] == f"User '{fake_user_id_2}' not found!"

    stmt = select(fat).where(
        fat.c.follower_id == user_id_1, fat.c.following_id == fake_user_id_2
    )
    db_response: Result = await db_session.execute(stmt)
    followers: fat | None = db_response.scalar_one_or_none()

    assert followers is None


@pytest.mark.asyncio
async def test_delete_follow_success(client, db_session):
    """Тест успешного запроса к API
    POST /api/users/{user_id}/follow
    """

    user_id_1 = users_correct[0]["id"]
    user_api_key_1 = users_correct[0]["api_key"]
    user_id_2 = users_correct[1]["id"]

    response = await client.delete(
        f"/api/users/{user_id_2}/follow", headers={"api-key": user_api_key_1}
    )
    data = response.json()

    assert response.status_code == 200
    assert data["result"] is True

    stmt = select(fat).where(
        fat.c.follower_id == user_id_1, fat.c.following_id == user_id_2
    )
    db_response: Result = await db_session.execute(stmt)
    followers: fat | None = db_response.scalar_one_or_none()

    assert followers is None
