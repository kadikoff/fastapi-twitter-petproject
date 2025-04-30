from pydantic import BaseModel, ConfigDict, field_validator


class MediasRead(BaseModel):
    result: bool = True
    media_id: int


class MediasAllRead(BaseModel):
    media_path: list[str]

    model_config = ConfigDict(serialize_by_alias=True)

    @field_validator("media_path", mode="before")
    def get_fields(cls, data):
        return [data.media_path]
