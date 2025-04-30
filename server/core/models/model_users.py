from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .model_base import Base

if TYPE_CHECKING:
    from .model_likes import Likes
    from .model_tweets import Tweets


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30))
    api_key: Mapped[str] = mapped_column(String(10), unique=True)

    tweets: Mapped[list["Tweets"]] = relationship(
        "Tweets", back_populates="user", cascade="all, delete-orphan"
    )
    likes: Mapped[list["Likes"]] = relationship("Likes", back_populates="user")

    def __repr__(self):
        return f"User: id={self.id}, name={self.name}, api_key={self.api_key}"
