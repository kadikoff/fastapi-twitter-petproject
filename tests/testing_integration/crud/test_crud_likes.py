import pytest
from fastapi import HTTPException
from sqlalchemy import Result, select

from server.api.crud import crud_likes
from server.core.models import Likes, Users
from tests.data.data_db_mock import users_correct


@pytest.mark.asyncio
async def test_create_like_success(db_session):
    """Тест успешного создания лайка к посту"""

    tweet_id = 2
    user_data = Users(**users_correct[0])

    await crud_likes.create_like(
        session=db_session, tweet_id=tweet_id, current_user=user_data
    )

    stmt = select(Likes).where(
        Likes.tweet_id == tweet_id, Likes.user_id == user_data.id
    )
    db_response: Result = await db_session.execute(stmt)
    like: Likes | None = db_response.scalar_one_or_none()

    assert like is not None
    assert isinstance(like, Likes)
    assert like.tweet_id == tweet_id
    assert like.user_id == user_data.id


@pytest.mark.asyncio
async def test_create_like_not_found_tweet_error(db_session):
    """Тест обработки ошибки при создании лайка
    к не существующему посту
    """

    tweet_id = 123456789
    user_data = Users(**users_correct[0])

    with pytest.raises(HTTPException) as exc_info:
        await crud_likes.create_like(
            session=db_session, tweet_id=tweet_id, current_user=user_data
        )

    stmt = select(Likes).where(
        Likes.tweet_id == tweet_id, Likes.user_id == user_data.id
    )
    db_response: Result = await db_session.execute(stmt)
    like: Likes | None = db_response.scalar_one_or_none()

    assert like is None
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == f"Tweet '{tweet_id}' not found!"


@pytest.mark.asyncio
async def test_delete_like_success(db_session):
    """Тест успешного удаления лайка к посту"""

    tweet_id = 2
    user_data = Users(**users_correct[0])

    await crud_likes.delete_like(
        session=db_session, tweet_id=tweet_id, current_user=user_data
    )

    stmt = select(Likes).where(
        Likes.tweet_id == tweet_id, Likes.user_id == user_data.id
    )
    db_response: Result = await db_session.execute(stmt)
    like: Likes | None = db_response.scalar_one_or_none()

    assert like is None
