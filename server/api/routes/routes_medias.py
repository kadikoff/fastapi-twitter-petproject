from typing import Annotated

from fastapi import APIRouter, Depends, Response, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from server.api.crud import crud_medias
from server.api.dependencies import authenticate_user
from server.core.models import Medias, Users, db_helper
from server.core.schemas.schemas_base import (
    NotFoundErrorResponse,
    ServerErrorResponse,
    UnauthorizedErrorResponse,
    ValidationErrorResponse,
)
from server.core.schemas.schemas_medias import MediasRead

router = APIRouter()


@router.post(
    "/api/medias",
    status_code=status.HTTP_201_CREATED,
    response_model=MediasRead,
    summary="Загрузить медиа-файлы",
    responses={
        401: {"model": UnauthorizedErrorResponse},
        404: {"model": NotFoundErrorResponse},
        422: {"model": ValidationErrorResponse},
        500: {"model": ServerErrorResponse},
    },
)
async def upload_medias(
    current_user: Annotated[Users, Depends(authenticate_user)],
    file: UploadFile,
    response: Response,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """Загрузить медиа-файлы

    1. Проверка авторизации текущего пользователя
    2. Получение сессии для базы данных
    3. Запись api_key текущего пользователя в заголовок ответа
    4. Добавление данных в таблицу бд
    """

    response.headers["api-key"] = current_user.api_key

    new_media: Medias = await crud_medias.create_media(
        session=session, file=file
    )

    return {"media_id": new_media.media_id}
