from fastapi import HTTPException, status
from sqlalchemy import Result, delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from server.core.models import Users, followers_association_table


async def get_user_by_api_key(
    session: AsyncSession, api_key: str
) -> Users | None:
    """Получение данных пользователя по его api_key
    из таблицы Users

    Вместе с получением данных о пользователе, из
    интеграционной таблицы followers_association_table
    подгружаются данные о подписчиках и подписках.

    Если пользователь не авторизован - возникает ошибка.

    Используется в зависимости по аутентификации пользователя,
    там проверяется - существует ли пользователь в системе
    с текущим api_key или нет.

    Далее данные о текущем пользователе используются и в других методах.
    """

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
    """Получение данных о пользователе по его user_id из таблицы Users

    Если пользователь по текущему id не найден - возникает ошибка.

    Используется в эндпоинте:
    - GET /api/users/{user_id} - получить информацию о пользователе по его id
    """

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
    """Создание подписки текущего пользователя на другого
    в таблице followers_association_table

    Если второго пользователя не существует в системе -
    возникает ошибка.

    Используется в эндпоинте:
    - POST /api/users/{user_id}/follow -
    создать подписку на другого пользователя
    """

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
    """Удаление подписки текущего пользователя на другого
    из таблицы followers_association_table

    Используется в эндпоинте:
    - DELETE /api/users/{user_id}/follow -
    удалить подписку на другого пользователя
    """

    stmt = delete(followers_association_table).where(
        followers_association_table.c.follower_id == current_user.id,
        followers_association_table.c.following_id == user_id,
    )
    await session.execute(stmt)
    await session.commit()
