from typing import Annotated

from fastapi import APIRouter, Depends, Path, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from server.api.crud import crud_users
from server.api.dependencies import authenticate_user
from server.core.models import Users, db_helper
from server.core.schemas.schemas_base import NotFoundResponse
from server.core.schemas.schemas_users import UserRead

router = APIRouter()


@router.get(
    "/api/users/me",
    status_code=status.HTTP_200_OK,
    response_model=UserRead,
)
async def get_me(
    current_user: Annotated[Users, Depends(authenticate_user)],
    response: Response,
):
    response.headers["api-key"] = current_user.api_key
    return {"user": current_user}


@router.get(
    "/api/users/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserRead,
    responses={404: {"model": NotFoundResponse}},
)
async def get_user(
    user_id: Annotated[int, Path(ge=1)],
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    user = await crud_users.get_user_by_id(user_id=user_id, session=session)
    return {"user": user}
