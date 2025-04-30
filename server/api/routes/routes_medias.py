from typing import Annotated

from fastapi import APIRouter, Depends, Response, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from server.api.crud import crud_medias
from server.api.dependencies import authenticate_user
from server.core.models import Users, db_helper
from server.core.schemas.schemas_base import NotFoundResponse
from server.core.schemas.schemas_medias import MediasRead

router = APIRouter()


@router.post(
    "/api/medias",
    status_code=status.HTTP_201_CREATED,
    response_model=MediasRead,
    responses={404: {"model": NotFoundResponse}},
)
async def upload_medias(
    current_user: Annotated[Users, Depends(authenticate_user)],
    file: UploadFile,
    response: Response,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    response.headers["api-key"] = current_user.api_key

    new_media = await crud_medias.create_media(session=session, file=file)
    return {"media_id": new_media.media_id}
