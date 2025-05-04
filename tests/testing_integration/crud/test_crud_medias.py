from pathlib import Path

import pytest
from fastapi import HTTPException
from sqlalchemy import Result, select

from server.api.crud import crud_medias
from server.core.models import Medias, Tweets
from server.utils.media_writer import delete_media


@pytest.mark.asyncio
async def test_create_media_success(db_session, sample_media_jpg):
    """Тест успешного создания медиа"""

    new_media: Medias = await crud_medias.create_media(
        session=db_session, file=sample_media_jpg
    )
    media_path = Path(new_media.media_path)

    assert new_media
    assert isinstance(new_media, Medias)
    assert media_path.exists()

    await delete_media(file_path=Path(new_media.media_path))
    assert not media_path.exists()


@pytest.mark.asyncio
async def test_create_media_not_allowed_ext_error(
    db_session, sample_media_pdf
):
    """Тест обработки ошибки при создании медиа
    с неподдерживаемым расширением файла
    """

    with pytest.raises(HTTPException) as exc_info:
        await crud_medias.create_media(
            session=db_session, file=sample_media_pdf
        )

    assert exc_info.value.status_code == 400


@pytest.mark.asyncio
async def test_update_media_success(db_session):
    """Тест успешного обновления медиа"""

    db_response: Result = await db_session.execute(select(Tweets).limit(1))
    tweet: Tweets = db_response.scalar()

    assert tweet is not None

    db_response: Result = await db_session.execute(select(Medias).limit(1))
    media: Medias = db_response.scalar()
    tweet_media_ids = [media.media_id]

    assert media is not None

    await crud_medias.update_media(
        session=db_session, tweet=tweet, tweet_media_ids=tweet_media_ids
    )

    assert media.tweet_id == tweet.tweet_id
