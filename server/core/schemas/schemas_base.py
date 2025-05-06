from fastapi import status
from pydantic import BaseModel, Field


class BaseResponse(BaseModel):
    """Схема для ответа API при успешном запросе

    Используется в эндпоинтах:
    - /api/users
        - POST /api/users/{user_id}/follow - создать подписку
        на другого пользователя
        - DELETE /api/users/{user_id}/follow - удалить подписку
        на другого пользователя
    - /api/tweets
        - DELETE /api/tweets/{tweet_id} - удалить твит
        - POST /api/tweets/{tweet_id}/likes - создать лайк на твит
        - DELETE /api/tweets/{tweet_id}/likes - удалить лайк с твита
    """

    result: bool = Field(
        description="Результат успешного ответа",
        default=True,
        examples=[True],
    )


class BaseErrorResponse(BaseModel):
    """Вложенная схема для ответа API при неуспешном запросе"""

    result: bool = Field(
        description="Результат неуспешного ответа",
        default=False,
        examples=[False],
    )


class BadRequestErrorResponse(BaseErrorResponse):
    """Схема для ответа API, когда сервер не может обработать
    запрос из-за ошибок на стороне клиента

    Используется в эндпоинте:
    - POST /api/medias - загрузить медиа-файлы
    """

    error_type: int = Field(
        description="Статус код ошибки",
        default=status.HTTP_400_BAD_REQUEST,
    )
    error_message: str = Field(
        description="Сообщение об ошибке",
        default="Invalid file format! Acceptable: ...",
    )


class UnauthorizedErrorResponse(BaseErrorResponse):
    """Схема для ответа API при неуспешном запросе api_key

    Используется во всех эндпоинтах, кроме GET /api/users/{user_id}
    """

    error_type: int = Field(
        description="Статус код ошибки",
        default=status.HTTP_401_UNAUTHORIZED,
    )
    error_message: str = Field(
        description="Сообщение об ошибке",
        default="API Key Authentication failed!",
    )


class NotFoundErrorResponse(BaseErrorResponse):
    """Схема для ответа API при неуспешном запросе,
    когда запрашиваемый ресурс не был найден

    Используется в эндпоинтах:
    - /api/users
        - GET /api/users/{user_id} - получить информацию
        о пользователе по его id
        - POST /api/users/{user_id}/follow - создать подписку
        на другого пользователя
        - DELETE /api/users/{user_id}/follow - удалить подписку
        на другого пользователя
    - /api/tweets
        - DELETE /api/tweets/{tweet_id} - удалить твит
        - POST /api/tweets/{tweet_id}/likes - создать лайк на твит
    - /api/medias
        - POST /api/medias - загрузить медиа-файлы
    """

    error_type: int = Field(
        description="Статус код ошибки",
        default=status.HTTP_404_NOT_FOUND,
    )
    error_message: str = Field(
        description="Сообщение об ошибке",
        default="<Resource> <id> not found!",
        examples=["User 1 not found!", "Tweet 1 not found!"],
    )


class ForbiddenErrorResponse(BaseErrorResponse):
    """Схема для ответа API при неуспешном запросе,
    когда у пользователя нет доступа/прав на выполнения
    определенных действий

    Используется в эндпоинтах:
    - DELETE /api/tweets/{tweet_id} - удалить твит
    """

    error_type: int = Field(
        description="Статус код ошибки",
        default=status.HTTP_403_FORBIDDEN,
    )
    error_message: str = Field(
        description="Сообщение об ошибке",
        examples=["You don't have permission to delete the tweet '1'!"],
    )


class ValidationErrorResponse(BaseErrorResponse):
    """Схема для ответа API при неуспешном запросе,
    когда данные невалидны, т.е. не удовлетворяют
    требованиям pydantic-схем

    Используется во всех эндпоинтах
    """

    error_type: int = Field(
        description="Статус код ошибки",
        default=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )
    error_message: str = Field(
        description="Сообщение об ошибке",
        default="Invalid data",
    )


class ServerErrorResponse(BaseErrorResponse):
    """Схема для ответа API при неуспешном запросе,
    когда иные ошибки возникают на стороне сервера

    Используется во всех эндпоинтах
    """

    error_type: int = Field(
        description="Статус код ошибки",
        default=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
    error_message: str = Field(
        description="Сообщение об ошибке",
        default="Server error",
    )
