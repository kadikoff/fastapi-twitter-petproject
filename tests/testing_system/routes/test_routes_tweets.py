import json

import pytest
from sqlalchemy import Result, select

from server.core.models import Likes, Tweets
from tests.data.data_db_for_tests import (
    tweet_media_valid,
    tweet_no_data_invalid,
)
from tests.data.data_db_mock import users_correct


@pytest.mark.asyncio
async def test_create_tweet_success(client, db_session):
    """Тест успешного запроса к API
    POST /api/tweets с использованием
    валидных данных (с текстом, с медиа)
    """

    user_api_key_1 = users_correct[0]["api_key"]
    tweet_data_json = json.dumps(tweet_media_valid)

    response = await client.post(
        "/api/tweets",
        content=tweet_data_json,
        headers={"api-key": user_api_key_1},
    )
    data = response.json()
    tweet_id = data["tweet_id"]

    assert response.status_code == 201
    assert data["result"] is True
    assert tweet_id

    tweet: Tweets | None = await db_session.get(Tweets, tweet_id)

    assert tweet is not None
    assert tweet.tweet_id == tweet_id
    assert tweet.tweet_data == tweet_media_valid["tweet_data"]
    assert tweet.user_id == users_correct[0]["id"]


@pytest.mark.asyncio
async def test_create_tweet_no_data_error(client, db_session):
    """Тест обработки ошибки при запросе к API
    POST /api/tweets с использованием
    невалидных данных (без текста, без медиа)
    """

    user_api_key_1 = users_correct[0]["api_key"]
    tweet_data_json = json.dumps(tweet_no_data_invalid)

    response = await client.post(
        "/api/tweets",
        content=tweet_data_json,
        headers={"api-key": user_api_key_1},
    )
    data = response.json()

    errors = data["error_message"][0]
    assert response.status_code == 422
    assert data["result"] is False
    assert data["error_type"] == 422
    assert errors["ctx"] == {"min_length": 1}
    assert errors["loc"] == ["body", "tweet_data"]
    assert errors["msg"] == "String should have at least 1 character"


@pytest.mark.asyncio
async def test_get_tweets_success(client):
    """Тест успешного запроса к API
    GET /api/tweets
    """

    user_api_key = users_correct[0]["api_key"]

    response = await client.get(
        "/api/tweets", headers={"api-key": user_api_key}
    )
    data = response.json()

    assert response.status_code == 200
    assert data["result"] is True


@pytest.mark.asyncio
async def test_delete_tweet_success(client, db_session):
    """Тест успешного обращения к API
    DELETE /api/tweets
    """

    user_api_key = users_correct[0]["api_key"]
    tweet_id = 4

    response = await client.delete(
        f"/api/tweets/{tweet_id}", headers={"api-key": user_api_key}
    )
    data = response.json()

    assert response.status_code == 200
    assert data["result"] is True

    tweet: Tweets | None = await db_session.get(Tweets, tweet_id)

    assert tweet is None


@pytest.mark.asyncio
async def test_delete_tweet_not_found_error(client, db_session):
    """Тест обработки ошибки при обращении к API
    DELETE /api/tweets с удалением несуществующего твита
    """

    user_api_key = users_correct[0]["api_key"]
    tweet_id = 1

    response = await client.delete(
        f"/api/tweets/{tweet_id}", headers={"api-key": user_api_key}
    )
    data = response.json()

    assert response.status_code == 404
    assert data["result"] is False

    tweet: Tweets | None = await db_session.get(Tweets, tweet_id)

    assert tweet is None


@pytest.mark.asyncio
async def test_delete_tweet_alien_error(client, db_session):
    """Тест обработки ошибки при обращении к API
    DELETE /api/tweets с удалением чужого твита
    """

    user_api_key = users_correct[0]["api_key"]
    tweet_id = 2

    response = await client.delete(
        f"/api/tweets/{tweet_id}", headers={"api-key": user_api_key}
    )
    data = response.json()

    assert response.status_code == 403
    assert data["result"] is False

    tweet: Tweets | None = await db_session.get(Tweets, tweet_id)

    assert tweet is not None


@pytest.mark.asyncio
async def test_create_like_success(client, db_session):
    """Тест успешного обращения к API
    POST /api/tweets/{tweet_id}/likes
    """

    user_api_key = users_correct[0]["api_key"]
    user_id = users_correct[0]["id"]
    tweet_id = 2

    response = await client.post(
        f"/api/tweets/{tweet_id}/likes", headers={"api-key": user_api_key}
    )
    data = response.json()

    assert response.status_code == 201
    assert data["result"] is True

    stmt = select(Likes).where(
        Likes.tweet_id == tweet_id, Likes.user_id == user_id
    )
    db_response: Result = await db_session.execute(stmt)
    like: Likes | None = db_response.scalar_one_or_none()

    assert like is not None
    assert isinstance(like, Likes)
    assert like.tweet_id == tweet_id
    assert like.user_id == user_id


@pytest.mark.asyncio
async def test_create_like_not_found_tweet_error(client, db_session):
    """Тест обработки при запросе к API
    POST /api/tweets/{tweet_id}/likes с использованием
    tweet_id несуществующего твита
    """

    user_api_key = users_correct[0]["api_key"]
    user_id = users_correct[0]["id"]
    tweet_id = 123456789

    response = await client.post(
        f"/api/tweets/{tweet_id}/likes", headers={"api-key": user_api_key}
    )
    data = response.json()

    assert response.status_code == 404
    assert data["result"] is False
    assert data["error_type"] == 404
    assert data["error_message"] == f"Tweet '{tweet_id}' not found!"

    stmt = select(Likes).where(
        Likes.tweet_id == tweet_id, Likes.user_id == user_id
    )
    db_response: Result = await db_session.execute(stmt)
    like: Likes | None = db_response.scalar_one_or_none()

    assert like is None


@pytest.mark.asyncio
async def test_delete_like_success(client, db_session):
    """Тест успешного обращения к API
    DELETE /api/tweets/{tweet_id}/likes
    """

    user_api_key = users_correct[0]["api_key"]
    user_id = users_correct[0]["id"]
    tweet_id = 2

    response = await client.delete(
        f"/api/tweets/{tweet_id}/likes", headers={"api-key": user_api_key}
    )
    data = response.json()

    assert response.status_code == 200
    assert data["result"] is True

    stmt = select(Likes).where(
        Likes.tweet_id == tweet_id, Likes.user_id == user_id
    )
    db_response: Result = await db_session.execute(stmt)
    like: Likes | None = db_response.scalar_one_or_none()

    assert like is None
