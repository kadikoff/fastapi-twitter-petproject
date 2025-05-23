from typing import Annotated

from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from server.api.crud import crud_users
from server.core.dependencies.authenticate import authenticate_user
from server.core.models import Users, db_helper
from server.core.schemas.schemas_base import (
    BaseResponse,
    NotFoundErrorResponse,
    ServerErrorResponse,
    UnauthorizedErrorResponse,
    ValidationErrorResponse,
)
from server.core.schemas.schemas_users import UserRead

router = APIRouter()


@router.get(
    "/api/users/me",
    status_code=status.HTTP_200_OK,
    summary="Получить информацию о себе (о текущем пользователе)",
    response_model=UserRead,
    responses={
        401: {"model": UnauthorizedErrorResponse},
        422: {"model": ValidationErrorResponse},
        500: {"model": ServerErrorResponse},
    },
)
async def get_me(
    current_user: Annotated[Users, Depends(authenticate_user)],
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """Получить информацию о себе (о текущем пользователе)

    1. Проверка авторизации текущего пользователя
    1.1. Запрос данных из бд
    2. Запись api_key текущего пользователя в заголовок ответа
    """

    user: Users | None = await crud_users.get_user_by_id(
        user_id=current_user.id, session=session
    )

    return {"user": user}


@router.get(
    "/api/users/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserRead,
    summary="Получить информацию о пользователе по его id",
    responses={
        404: {"model": NotFoundErrorResponse},
        422: {"model": ValidationErrorResponse},
        500: {"model": ServerErrorResponse},
    },
)
async def get_user(
    user_id: Annotated[int, Path(ge=1)],
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """Получить информацию о пользователе по его id

    1. Валидация user_id запрашиваемого пользователя
    2. Получение сессии для базы данных
    3. Запрос данных из бд
    """

    user: Users | None = await crud_users.get_user_by_id(
        user_id=user_id, session=session
    )

    return {"user": user}


@router.post(
    "/api/users/{user_id}/follow",
    status_code=status.HTTP_200_OK,
    response_model=BaseResponse,
    summary="Создать подписку на другого пользователя",
    responses={
        401: {"model": UnauthorizedErrorResponse},
        404: {"model": NotFoundErrorResponse},
        422: {"model": ValidationErrorResponse},
        500: {"model": ServerErrorResponse},
    },
)
async def create_follow(
    current_user: Annotated[Users, Depends(authenticate_user)],
    user_id: Annotated[int, Path(ge=1)],
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """Создать подписку на другого пользователя

    1. Проверка авторизации текущего пользователя
    2. Валидация user_id запрашиваемого пользователя
    3. Получение сессии для базы данных
    4. Запись api_key текущего пользователя в заголовок ответа
    5. Добавление данных в таблицу бд
    """

    await crud_users.create_follow(
        session=session, current_user=current_user, user_id=user_id
    )

    return {"result": True}


@router.delete(
    "/api/users/{user_id}/follow",
    status_code=status.HTTP_200_OK,
    response_model=BaseResponse,
    summary="Удалить подписку на другого пользователя",
    responses={
        401: {"model": UnauthorizedErrorResponse},
        404: {"model": NotFoundErrorResponse},
        422: {"model": ValidationErrorResponse},
        500: {"model": ServerErrorResponse},
    },
)
async def delete_follow(
    current_user: Annotated[Users, Depends(authenticate_user)],
    user_id: Annotated[int, Path(ge=1)],
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """Удалить подписку на другого пользователя

    1. Проверка авторизации текущего пользователя
    2. Валидация user_id запрашиваемого пользователя
    3. Получение сессии для базы данных
    4. Запись api_key текущего пользователя в заголовок ответа
    5. Удаление данных из таблицы бд
    """

    await crud_users.delete_follow(
        session=session, current_user=current_user, user_id=user_id
    )

    return {"result": True}
