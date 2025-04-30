from fastapi import Depends, Security
from fastapi.security import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession

from server.api.crud import crud_users
from server.core.models import Users, db_helper

API_KEY_HEADER = APIKeyHeader(name="api-key")


async def authenticate_user(
    session: AsyncSession = Depends(db_helper.session_dependency),
    api_key: str = Security(API_KEY_HEADER),
) -> Users | None:

    return await crud_users.get_user_by_api_key(
        session=session, api_key=api_key
    )
