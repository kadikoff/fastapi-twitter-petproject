from pydantic import BaseModel, ConfigDict, Field, model_validator


class BaseLikes(BaseModel):
    """Вложенная схема с информацией о лайках"""

    id: int = Field(
        description="Уникальный идентификатор пользователя в системе",
        serialization_alias="user_id",
        examples=[2],
    )
    name: str = Field(
        description="Имя пользователя",
        examples=["Nikita Ivanov"],
    )

    model_config = ConfigDict(serialize_by_alias=True)

    @model_validator(mode="before")
    @classmethod
    def get_user_data(cls, data):
        return {"id": data.user.id, "name": data.user.name}
