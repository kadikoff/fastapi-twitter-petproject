from typing import Annotated

from fastapi import APIRouter, Depends, Path, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

import server.api.crud.crud_likes
from server.api.crud import crud_tweets
from server.api.dependencies import authenticate_user
from server.core.models import Users, db_helper
from server.core.schemas.schemas_base import BaseResponse, NotFoundResponse
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
    responses={404: {"model": NotFoundResponse}},
)
async def create_tweet(
    current_user: Annotated[Users, Depends(authenticate_user)],
    tweet_in: TweetCreate,
    response: Response,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    response.headers["api-key"] = current_user.api_key
    return await crud_tweets.create_tweet(
        session=session, user=current_user, tweet_in=tweet_in
    )


@router.get(
    "/api/tweets",
    status_code=status.HTTP_200_OK,
    response_model=TweetsRead,
    responses={404: {"model": NotFoundResponse}},
)
async def get_tweets(
    current_user: Annotated[Users, Depends(authenticate_user)],
    response: Response,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    response.headers["api-key"] = current_user.api_key
    tweets = await crud_tweets.get_tweets(session=session)

    return {"tweets": tweets}


@router.delete(
    "/api/tweets/{tweet_id}",
    status_code=status.HTTP_200_OK,
    response_model=BaseResponse,
)
async def delete_tweet(
    current_user: Annotated[Users, Depends(authenticate_user)],
    tweet_id: Annotated[int, Path(ge=1)],
    response: Response,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    response.headers["api-key"] = current_user.api_key
    await crud_tweets.delete_tweet(
        session=session, tweet_id=tweet_id, current_user=current_user
    )

    return {"result": True}


@router.post(
    "/api/tweets/{tweet_id}/likes",
    status_code=status.HTTP_201_CREATED,
    response_model=BaseResponse,
)
async def create_like(
    current_user: Annotated[Users, Depends(authenticate_user)],
    tweet_id: Annotated[int, Path(ge=1)],
    response: Response,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    response.headers["api-key"] = current_user.api_key
    await server.api.crud.crud_likes.create_like(
        session=session, tweet_id=tweet_id, current_user=current_user
    )

    return {"result": True}


@router.delete(
    "/api/tweets/{tweet_id}/likes",
    status_code=status.HTTP_200_OK,
    response_model=BaseResponse,
)
async def delete_like(
    current_user: Annotated[Users, Depends(authenticate_user)],
    tweet_id: Annotated[int, Path(ge=1)],
    response: Response,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    response.headers["api-key"] = current_user.api_key
    await server.api.crud.crud_likes.delete_like(
        session=session, tweet_id=tweet_id, current_user=current_user
    )

    return {"result": True}
