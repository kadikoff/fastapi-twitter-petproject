import pytest
from pydantic import ValidationError

from server.api.crud import crud_tweets, crud_users
from server.core.models import Tweets, Users
from server.core.schemas.schemas_tweets import (
    TweetCreate,
    TweetRead,
    TweetsRead,
)
from tests.data.data_db_for_tests import (
    tweet_media_valid,
    tweet_no_data_invalid,
)


def test_tweet_create_success():
    """Тест успешной валидации данных
    по схеме TweetCreate с использованием валидных данных
    """

    tweet_data = TweetCreate(**tweet_media_valid)
    user_data_dict: dict = tweet_data.model_dump()

    assert tweet_data is not None
    assert user_data_dict == tweet_media_valid


def test_tweet_create_invalid_error():
    """Тест обработки ошибки при валидации
    данных по схеме TweetCreate с использованием
    невалидных данных
    """

    with pytest.raises(ValidationError) as exc_info:
        TweetCreate(**tweet_no_data_invalid)

    errors = exc_info.value.errors()
    assert len(errors) == 1, errors

    assert errors[0]["loc"] == ("tweet_data",)
    assert errors[0]["ctx"] == {"min_length": 1}
    assert "String should have at least 1 character" in errors[0]["msg"]


@pytest.mark.asyncio
async def test_tweet_read_success(db_session):
    """Тест успешной валидации данных
    по схеме TweetRead с использованием валидных данных
    """

    tweet: Tweets = await db_session.get(Tweets, 2)
    assert tweet is not None

    tweet_read = TweetRead.model_validate(tweet, from_attributes=True)

    assert tweet_read
    assert isinstance(tweet_read, TweetRead)
    assert tweet_read.result
    assert tweet_read.tweet_id == tweet.tweet_id


def test_tweet_read_invalid_error():
    """Тест обработки ошибки при валидации
    данных по схеме TweetRead с использованием
    невалидных данных
    """

    with pytest.raises(ValidationError) as exc_info:
        TweetRead(**tweet_no_data_invalid)

    errors = exc_info.value.errors()
    assert len(errors) == 1

    assert errors[0]["loc"] == ("tweet_id",)
    assert errors[0]["type"] == "missing"
    assert "Field required" in errors[0]["msg"]


@pytest.mark.asyncio
async def test_tweets_read_success(db_session):
    """Тест успешной валидации данных
    по схеме TweetsRead с использованием валидных данных
    """

    user: Users | None = await crud_users.get_user_by_id(
        session=db_session, user_id=1
    )
    assert user is not None

    offset = 0
    limit = 50

    tweets: list[Tweets | None] = await crud_tweets.get_tweets(
        session=db_session,
        current_user=user,
        offset=offset,
        limit=limit,
    )
    assert tweets is not None

    tweets_data = {"tweets": tweets}
    tweets_read = TweetsRead.model_validate(tweets_data, from_attributes=True)

    assert tweets_read
    assert isinstance(tweets_read, TweetsRead)
    assert tweets_read.result

    assert tweets_read.tweets
    assert tweets_read.tweets[0].tweet_id == tweets[0].tweet_id
