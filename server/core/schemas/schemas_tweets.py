from pydantic import BaseModel, ConfigDict, Field, field_validator

from server.core.models import Medias

from .schemas_likes import BaseLikes
from .schemas_users import BaseUser


class BaseTweet(BaseModel):
    tweet_id: int = Field(serialization_alias="id")
    tweet_data: str = Field(serialization_alias="content")
    medias: list[str] = Field(serialization_alias="attachments")
    user: BaseUser = Field(serialization_alias="author")
    likes: list[BaseLikes]

    model_config = ConfigDict(serialize_by_alias=True)

    @field_validator("medias", mode="before")
    def get_fields(cls, data: list[Medias]):
        return [media.media_path for media in data]


class TweetsRead(BaseModel):
    result: bool = True
    tweets: list[BaseTweet]


class TweetCreate(BaseModel):
    tweet_data: str
    tweet_media_ids: list[int] | None


class TweetRead(BaseModel):
    result: bool = True
    tweet_id: int
