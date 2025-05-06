from pydantic import BaseModel, Field


class BaseUser(BaseModel):
    """Вложенная схема с базовой информацией о пользователе"""

    id: int = Field(
        description="Уникальный идентификатор пользователя в системе",
        ge=1,
        examples=[1],
    )
    name: str = Field(
        description="Имя пользователя в системе",
        examples=["Aleksey Owner"],
    )


class BaseUserFollowers(BaseUser):
    """Вложенная схема с информацией о пользователях,
    которые подписаны на текущего и на которых подписан он
    """

    followers: list[BaseUser] = Field(
        description="Список пользователей, которые подписаны на текущего",
        examples=[[{"id": 2, "name": "Nikita Ivanov"}]],
    )
    following: list[BaseUser] = Field(
        description="Список пользователей, на которых подписан текущий",
        examples=[[{"id": 3, "name": "Ivan Volkov"}]],
    )


class UserRead(BaseModel):
    """Схема для ответа API при запросе информации о пользователе

    Используется в эндпоинтах:
    - GET /api/users/me - получить информацию о себе
    - GET /api/users/{user_id} - получить информацию о пользователе по его id
    """

    result: bool = Field(
        description="Результат успешного ответа",
        default=True,
        examples=[True],
    )
    user: BaseUserFollowers = Field(
        description="Полная информация о пользователе"
    )
