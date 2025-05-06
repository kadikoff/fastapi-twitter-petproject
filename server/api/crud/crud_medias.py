from pathlib import Path

from fastapi import UploadFile
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from server.core.models import Medias, Tweets
from server.utils.media_writer import save_media


async def create_media(session: AsyncSession, file: UploadFile) -> Medias:
    """Создание записи в таблице Medias - сохранение пути до медиа-файла

    Используется в момент, когда пользователь выкладывает твит
    с медиа-файлом - создаётся запись в таблице с указанием
    пути до медиа-файла (media_path) на сервере, чтобы в дальнейшем
    при get-запросах подгрузить те самые медиа-файлы, зная их путь.

    Используется в эндпоинте:
    - POST /api/medias - загрузить медиа-файлы
    """

    file_path: Path | None = await save_media(file=file)
    new_media = Medias(media_path=str(file_path))
    session.add(new_media)
    await session.commit()

    return new_media


async def update_media(
    session: AsyncSession, tweet: Tweets, tweet_media_ids: list[int]
) -> None:
    """Обновление записи в таблице Medias - привязка медиа-файлов
    к твитам через колонку tweet_id в таблице Medias

    Используется в crud-методе по созданию твита - create_tweet
    """

    stmt = (
        update(Medias)
        .where(Medias.media_id.in_(tweet_media_ids))
        .values(tweet_id=tweet.tweet_id)
    )

    await session.execute(stmt)
    await session.commit()
