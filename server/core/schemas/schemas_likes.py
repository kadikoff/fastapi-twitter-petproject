from pydantic import BaseModel, ConfigDict, Field, model_validator


class BaseLikes(BaseModel):
    id: int = Field(serialization_alias="user_id")
    name: str

    model_config = ConfigDict(serialize_by_alias=True)

    @model_validator(mode="before")
    @classmethod
    def get_user_data(cls, data):
        return {"id": data.user.id, "name": data.user.name}
