from pydantic import BaseModel, Field


class MediasRead(BaseModel):
    """Схема для ответа API при загрузке медиа-файлов

    Используется в эндпоинтах:
    - POST /api/medias - загрузка медиа-файлов
    """

    result: bool = Field(
        description="Результат успешного ответа",
        default=True,
        examples=[True],
    )
    media_id: int = Field(
        description="Уникальный идентификатор медиа-файла в системе",
        ge=1,
        examples=[1],
    )
