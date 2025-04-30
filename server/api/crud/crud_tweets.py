from fastapi import HTTPException, status
from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from server.api.crud import crud_medias
from server.core.models import Likes, Tweets, Users
from server.core.schemas.schemas_tweets import TweetCreate


async def create_tweet(
    session: AsyncSession, user: Users, tweet_in: TweetCreate
) -> Tweets:

    new_tweet = Tweets(tweet_data=tweet_in.tweet_data, user_id=user.id)
    session.add(new_tweet)

    if tweet_in.tweet_media_ids:
        await session.flush()
        await crud_medias.update_media(
            session=session,
            tweet=new_tweet,
            tweet_media_ids=tweet_in.tweet_media_ids,
        )

    await session.commit()
    return new_tweet


async def get_tweets(
    session: AsyncSession, current_user: Users
) -> list[Tweets] | None:

    following_ids: list[int] = [user.id for user in current_user.following]
    following_ids.append(current_user.id)

    stmt = (
        select(Tweets, func.count(Tweets.likes).label("count_likes"))
        .filter(Tweets.user_id.in_(following_ids))
        .options(
            joinedload(Tweets.user),
            joinedload(Tweets.likes).subqueryload(Likes.user),
            joinedload(Tweets.medias),
        )
        .outerjoin(Tweets.likes)
        .group_by(Tweets)
        .order_by(desc("count_likes"))
    )

    db_response = await session.execute(stmt)
    tweets = db_response.unique().scalars().all()

    return list(tweets)


async def delete_tweet(
    session: AsyncSession, tweet_id: int, current_user: Users
) -> None:

    tweet: Tweets | None = await session.get(Tweets, tweet_id)
    if not tweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tweet '{tweet_id}' not found!",
        )

    if tweet.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You don't have permission "
            f"to delete the tweet '{tweet_id}'!",
        )

    await session.delete(tweet)
    await session.commit()
