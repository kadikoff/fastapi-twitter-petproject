from pydantic import BaseModel


class BaseUser(BaseModel):
    id: int
    name: str


class BaseUserFollowers(BaseUser):
    followers: list[BaseUser]
    following: list[BaseUser]


class UserRead(BaseModel):
    result: bool = True
    user: BaseUserFollowers
