from fastapi import status
from pydantic import BaseModel


class BaseResponse(BaseModel):
    result: bool


class NotFoundResponse(BaseResponse):

    error_type: int = status.HTTP_404_NOT_FOUND
    error_message: str
