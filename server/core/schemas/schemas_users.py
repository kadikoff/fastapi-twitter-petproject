from pydantic import BaseModel


class BaseUser(BaseModel):
    id: int
    name: str


class UserRead(BaseModel):
    result: bool = True
    user: BaseUser
