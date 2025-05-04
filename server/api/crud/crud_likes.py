from fastapi import HTTPException, status
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from server.core.models import Likes, Tweets, Users


async def create_like(
    session: AsyncSession, tweet_id: int, current_user: Users
) -> None:

    tweet: Tweets | None = await session.get(Tweets, tweet_id)
    if not tweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tweet '{tweet_id}' not found!",
        )

    new_like = Likes(tweet_id=tweet_id, user_id=current_user.id)

    session.add(new_like)
    await session.commit()


async def delete_like(
    session: AsyncSession, tweet_id: int, current_user: Users
) -> None:

    stmt = select(Likes).where(
        Likes.tweet_id == tweet_id, Likes.user_id == current_user.id
    )
    db_response: Result = await session.execute(stmt)
    like: Likes | None = db_response.scalar_one_or_none()

    await session.delete(like)
    await session.commit()
