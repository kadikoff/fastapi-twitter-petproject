from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .model_base import Base

if TYPE_CHECKING:
    from .model_likes import Likes
    from .model_medias import Medias
    from .model_users import Users


class Tweets(Base):
    __tablename__ = "tweets"

    tweet_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tweet_data: Mapped[str] = mapped_column(String(100))
    user_id: Mapped[int] = mapped_column(ForeignKey(column="users.id"))

    user: Mapped[list["Users"]] = relationship(
        "Users", back_populates="tweets"
    )
    likes: Mapped[list["Likes"]] = relationship(
        "Likes", back_populates="tweet", cascade="all, delete-orphan"
    )
    medias: Mapped[list["Medias"]] = relationship(
        "Medias", back_populates="tweet", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return (
            f"Tweet: id={self.tweet_id}, "
            f"tweet_data={self.tweet_data}, "
            f"user_id={self.user_id}"
        )
