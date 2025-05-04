from fastapi import HTTPException, status
from sqlalchemy import Result, delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from server.core.models import Users, followers_association_table


async def get_user_by_api_key(
    session: AsyncSession, api_key: str
) -> Users | None:

    stmt = (
        select(Users)
        .where(Users.api_key == api_key)
        .options(
            joinedload(Users.followers),
            joinedload(Users.following),
        )
    )
    db_response: Result = await session.execute(stmt)

    user: Users | None = db_response.unique().scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key Authentication failed!",
        )

    return user


async def get_user_by_id(session: AsyncSession, user_id: int) -> Users | None:

    stmt = (
        select(Users)
        .where(Users.id == user_id)
        .options(
            joinedload(Users.followers),
            joinedload(Users.following),
        )
    )
    db_response: Result = await session.execute(stmt)

    user: Users | None = db_response.unique().scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User '{user_id}' not found!",
        )

    return user


async def create_follow(
    session: AsyncSession, current_user: Users, user_id: int
) -> None:

    following_user: Users | None = await session.get(Users, user_id)
    if not following_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User '{user_id}' not found!",
        )

    stmt = insert(followers_association_table).values(
        follower_id=current_user.id, following_id=user_id
    )
    await session.execute(stmt)
    await session.commit()


async def delete_follow(
    session: AsyncSession, current_user: Users, user_id: int
) -> None:

    stmt = delete(followers_association_table).where(
        followers_association_table.c.follower_id == current_user.id,
        followers_association_table.c.following_id == user_id,
    )
    await session.execute(stmt)
    await session.commit()
