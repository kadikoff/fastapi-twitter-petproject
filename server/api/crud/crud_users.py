from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from server.core.models import Users


async def get_user_by_api_key(
    session: AsyncSession, api_key: str
) -> Users | None:

    stmt = select(Users).where(Users.api_key == api_key)
    db_response = await session.execute(stmt)

    user = db_response.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key Authentication failed!",
        )

    return user


async def get_user_by_id(session: AsyncSession, user_id: int) -> Users | None:

    user: Users | None = await session.get(Users, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User '{user_id}' not found!",
        )

    return user
