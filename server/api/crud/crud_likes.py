from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from server.core.models import Likes, Users


async def create_like(
    session: AsyncSession, tweet_id: int, current_user: Users
) -> None:

    new_like = Likes(tweet_id=tweet_id, user_id=current_user.id)

    session.add(new_like)
    await session.commit()


async def delete_like(
    session: AsyncSession, tweet_id: int, current_user: Users
) -> None:

    stmt = select(Likes).where(
        Likes.tweet_id == tweet_id, Likes.user_id == current_user.id
    )
    db_response = await session.execute(stmt)
    like = db_response.scalar_one_or_none()

    await session.delete(like)
    await session.commit()
