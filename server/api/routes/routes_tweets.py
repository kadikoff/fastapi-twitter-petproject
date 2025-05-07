from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Path, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from server.api.crud import crud_likes, crud_tweets
from server.core.dependencies.authenticate import authenticate_user
from server.core.models import Tweets, Users, db_helper
from server.core.schemas.schemas_base import (
    BaseResponse,
    ForbiddenErrorResponse,
    NotFoundErrorResponse,
    ServerErrorResponse,
    UnauthorizedErrorResponse,
    ValidationErrorResponse,
)
from server.core.schemas.schemas_tweets import (
    TweetCreate,
    TweetRead,
    TweetsRead,
)

router = APIRouter()


@router.post(
    "/api/tweets",
    status_code=status.HTTP_201_CREATED,
    response_model=TweetRead,
    summary="Создать твит",
    responses={
        401: {"model": UnauthorizedErrorResponse},
        422: {"model": ValidationErrorResponse},
        500: {"model": ServerErrorResponse},
    },
)
async def create_tweet(
    current_user: Annotated[Users, Depends(authenticate_user)],
    tweet_in: TweetCreate,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """Создать твит

    1. Проверка авторизации текущего пользователя
    2. Валидация данных создаваемого твита
    3. Получение сессии для базы данных
    4. Запись api_key текущего пользователя в заголовок ответа
    5. Добавление данных в таблицу бд
    """

    return await crud_tweets.create_tweet(
        session=session, user=current_user, tweet_in=tweet_in
    )


@router.get(
    "/api/tweets",
    status_code=status.HTTP_200_OK,
    response_model=TweetsRead,
    summary="Получить информации о всех твитах",
    responses={
        401: {"model": UnauthorizedErrorResponse},
        422: {"model": ValidationErrorResponse},
        500: {"model": ServerErrorResponse},
    },
)
async def get_tweets(
    current_user: Annotated[Users, Depends(authenticate_user)],
    offset: Annotated[
        Optional[int], Query(ge=1, description="Номер страницы (смещение)")
    ] = None,
    limit: Annotated[
        Optional[int], Query(ge=1, description="Количество твитов на странице")
    ] = None,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """Получить информации о всех твитах

    1. Проверка авторизации текущего пользователя
    2. Получение сессии для базы данных
    3. Запись api_key текущего пользователя в заголовок ответа
    4. Запрос данных из бд
    """

    default_offset = 0
    default_limit = 50

    tweets: list[Tweets | None] = await crud_tweets.get_tweets(
        session=session,
        current_user=current_user,
        offset=offset or default_offset,
        limit=limit or default_limit,
    )

    return {"tweets": tweets}


@router.delete(
    "/api/tweets/{tweet_id}",
    status_code=status.HTTP_200_OK,
    summary="Удалить твит",
    response_model=BaseResponse,
    responses={
        401: {"model": UnauthorizedErrorResponse},
        404: {"model": NotFoundErrorResponse},
        403: {"model": ForbiddenErrorResponse},
        422: {"model": ValidationErrorResponse},
        500: {"model": ServerErrorResponse},
    },
)
async def delete_tweet(
    current_user: Annotated[Users, Depends(authenticate_user)],
    tweet_id: Annotated[int, Path(ge=1)],
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """Удалить твит

    1. Проверка авторизации текущего пользователя
    2. Валидация tweet_id запрашиваемого твита
    3. Получение сессии для базы данных
    4. Запись api_key текущего пользователя в заголовок ответа
    5. Удаление данных из таблицы бд
    """

    await crud_tweets.delete_tweet(
        session=session, tweet_id=tweet_id, current_user=current_user
    )

    return {"result": True}


@router.post(
    "/api/tweets/{tweet_id}/likes",
    status_code=status.HTTP_201_CREATED,
    summary="Создать лайк на твит",
    response_model=BaseResponse,
    responses={
        401: {"model": UnauthorizedErrorResponse},
        404: {"model": NotFoundErrorResponse},
        422: {"model": ValidationErrorResponse},
        500: {"model": ServerErrorResponse},
    },
)
async def create_like(
    current_user: Annotated[Users, Depends(authenticate_user)],
    tweet_id: Annotated[int, Path(ge=1)],
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """Создать лайк на твит

    1. Проверка авторизации текущего пользователя
    2. Валидация tweet_id запрашиваемого твита
    3. Получение сессии для базы данных
    4. Запись api_key текущего пользователя в заголовок ответа
    5. Добавление данных в таблицу бд
    """

    await crud_likes.create_like(
        session=session, tweet_id=tweet_id, current_user=current_user
    )

    return {"result": True}


@router.delete(
    "/api/tweets/{tweet_id}/likes",
    status_code=status.HTTP_200_OK,
    summary="Удалить лайк с твита",
    response_model=BaseResponse,
    responses={
        401: {"model": UnauthorizedErrorResponse},
        422: {"model": ValidationErrorResponse},
        500: {"model": ServerErrorResponse},
    },
)
async def delete_like(
    current_user: Annotated[Users, Depends(authenticate_user)],
    tweet_id: Annotated[int, Path(ge=1)],
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """Удалить лайк с твита

    1. Проверка авторизации текущего пользователя
    2. Валидация tweet_id запрашиваемого твита
    3. Получение сессии для базы данных
    4. Запись api_key текущего пользователя в заголовок ответа
    5. Удаление данных из таблицы бд
    """

    await crud_likes.delete_like(
        session=session, tweet_id=tweet_id, current_user=current_user
    )

    return {"result": True}
