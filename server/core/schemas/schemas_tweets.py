from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
)

from server.core.models import Medias

from .schemas_likes import BaseLikes
from .schemas_users import BaseUser


class BaseTweet(BaseModel):
    """Вложенная схема с информацией о твите"""

    tweet_id: int = Field(
        description="Уникальный идентификатор твита в системе",
        serialization_alias="id",
        examples=[1],
    )
    tweet_data: str = Field(
        description="Текст для твита",
        serialization_alias="content",
        examples=["Hello world!"],
    )
    medias: list[str] = Field(
        description="Информация о медиа-файлах (путь до медиа-файла)",
        serialization_alias="attachments",
        examples=["/home/usr/bin/cat.jpg"],
    )
    user: BaseUser = Field(
        description="Информация о пользователе-авторе твита",
        serialization_alias="author",
    )
    likes: list[BaseLikes] = Field(
        description="Информация о лайках к твиту",
        examples=[
            [
                {"user_id": 2, "name": "Nikita Ivanov"},
                {"user_id": 3, "name": "Ivan Volkov"},
            ]
        ],
    )

    model_config = ConfigDict(serialize_by_alias=True)

    @field_validator("medias", mode="before")
    def get_fields(cls, data: list[Medias]):
        return [media.media_path for media in data]


class TweetsRead(BaseModel):
    """Схема для ответа API при запросе информации о твите

    Используется в эндпоинтах:
    - GET /api/tweets - получить информацию о всех твитах
    """

    result: bool = Field(
        description="Результат успешного ответа",
        default=True,
        examples=[True],
    )
    tweets: list[BaseTweet] = Field(description="Полная информация о твите")


class TweetCreate(BaseModel):
    """Схема для запроса к API при создании нового твита

    Используется в эндпоинтах:
    - POST /api/tweets - создать твит
    """

    tweet_data: str = Field(
        description="Текст для твита",
        min_length=1,
        max_length=100,
        examples=["Hello world!"],
    )
    tweet_media_ids: list[int] | None = Field(
        description="Список уникальных идентификаторов медиа-файлов",
        examples=[[1]],
    )


class TweetRead(BaseModel):
    """Схема для ответа API при создании твита

    Используется в эндпоинтах:
    - POST /api/tweets - создать твит
    """

    result: bool = Field(
        description="Результат успешного ответа",
        default=True,
        examples=[True],
    )
    tweet_id: int = Field(
        description="Уникальный идентификатор твита",
        examples=[1],
    )
