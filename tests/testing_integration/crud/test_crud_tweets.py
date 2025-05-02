import pytest
from fastapi import HTTPException
from pydantic import ValidationError

from server.api.crud import crud_tweets
from server.core.models import Tweets, Users
from server.core.schemas.schemas_tweets import TweetCreate
from tests.data.data_db_for_tests import (
    tweet_media_valid,
    tweet_no_data_invalid,
    tweet_no_media_valid,
)
from tests.data.data_db_mock import tweets_correct, users_correct


@pytest.mark.asyncio
async def test_create_tweet_no_media_success(db_session):
    """Тест успешного создания твита с использованием
    валидных данных (с текстом, без медиа)
    """

    user_data = Users(**users_correct[0])
    tweet_data = TweetCreate(**tweet_no_media_valid)

    new_tweet: Tweets = await crud_tweets.create_tweet(
        session=db_session, user=user_data, tweet_in=tweet_data
    )

    assert new_tweet
    assert isinstance(new_tweet, Tweets)
    assert new_tweet.tweet_data == tweet_data.tweet_data
    assert isinstance(new_tweet.tweet_data, str)


@pytest.mark.asyncio
async def test_create_tweet_media_success(db_session):
    """Тест успешного создания твита с использованием
    валидных данных (с текстом, с медиа)
    """

    user_data = Users(**users_correct[0])
    tweet_data = TweetCreate(**tweet_media_valid)

    new_tweet: Tweets = await crud_tweets.create_tweet(
        session=db_session, user=user_data, tweet_in=tweet_data
    )

    assert new_tweet
    assert isinstance(new_tweet, Tweets)
    assert new_tweet.tweet_data == tweet_data.tweet_data
    assert isinstance(new_tweet.tweet_data, str)


@pytest.mark.asyncio
async def test_create_tweet_no_data_error(db_session):
    """Тест обработки ошибки при создании твита
    (без текста, без медиа)
    """

    user_data = Users(**users_correct[0])

    with pytest.raises(ValidationError) as exc_info:
        tweet_data = TweetCreate(**tweet_no_data_invalid)
        await crud_tweets.create_tweet(
            session=db_session, user=user_data, tweet_in=tweet_data
        )

    errors = exc_info.value.errors()
    assert errors[0]["loc"] == ("tweet_data",)


@pytest.mark.asyncio
async def test_get_tweets_success(db_session):
    """Тест успешного получения твитов"""

    user_data = Users(**users_correct[0])

    new_tweet: list[Tweets] | None = await crud_tweets.get_tweets(
        session=db_session, current_user=user_data
    )

    assert new_tweet
    assert isinstance(new_tweet, list)


@pytest.mark.asyncio
async def test_delete_tweet_success(db_session):
    """Тест успешного удаления твита"""

    tweet_id = 1
    user_data = Users(**users_correct[0])

    await crud_tweets.delete_tweet(
        session=db_session, tweet_id=tweet_id, current_user=user_data
    )


@pytest.mark.asyncio
async def test_delete_tweet_not_found_error(db_session):
    """Тест обработки ошибки при удалении
    не существующего твита
    """

    tweet_id = 1
    user_data = Users(**users_correct[0])

    with pytest.raises(HTTPException) as exc_info:
        await crud_tweets.delete_tweet(
            session=db_session, tweet_id=tweet_id, current_user=user_data
        )

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == f"Tweet '{tweet_id}' not found!"


@pytest.mark.asyncio
async def test_delete_tweet_alien_error(db_session):
    """Тест обработки ошибки при удалении чужого твита"""

    alien_tweet: dict = tweets_correct[1]
    alien_user_id: int = alien_tweet["user_id"]
    alien_tweet_id: int = alien_tweet["tweet_id"]
    user_data = Users(**users_correct[0])

    assert alien_user_id != user_data.id

    with pytest.raises(HTTPException) as exc_info:
        await crud_tweets.delete_tweet(
            session=db_session, tweet_id=alien_tweet_id, current_user=user_data
        )

    exc_detail = (
        f"You don't have permission to delete the tweet '{alien_tweet_id}'!"
    )
    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == exc_detail
