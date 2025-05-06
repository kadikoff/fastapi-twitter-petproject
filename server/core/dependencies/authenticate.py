from fastapi import Depends, Response, Security
from fastapi.security import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession

from server.api.crud import crud_users
from server.core.models import Users, db_helper

API_KEY_HEADER = APIKeyHeader(name="api-key")


async def authenticate_user(
    response: Response,
    session: AsyncSession = Depends(db_helper.session_dependency),
    api_key: str = Security(API_KEY_HEADER),
) -> Users:
    """Зависимость для проверки существования пользователя
    по переданному api_key в заголовке для использования
    в FastAPI Depends
    """

    current_user: Users = await crud_users.get_user_by_api_key(
        session=session, api_key=api_key
    )

    response.headers["api-key"] = current_user.api_key

    return current_user
