from fastapi import UploadFile
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from server.core.models import Medias, Tweets
from server.utils.media_writer import save_media


async def create_media(session: AsyncSession, file: UploadFile):

    file_path = await save_media(file=file)
    new_media = Medias(media_path=str(file_path))
    session.add(new_media)
    await session.commit()

    return new_media


async def update_media(
    session: AsyncSession, tweet: Tweets, tweet_media_ids: list[int]
):

    stmt = (
        update(Medias)
        .where(Medias.media_id.in_(tweet_media_ids))
        .values(tweet_id=tweet.tweet_id)
    )

    await session.execute(stmt)
    await session.commit()
