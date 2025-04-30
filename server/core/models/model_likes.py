from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .model_base import Base

if TYPE_CHECKING:
    from .model_tweets import Tweets
    from .model_users import Users


class Likes(Base):
    __tablename__ = "likes"
    __table_args__ = (UniqueConstraint("tweet_id", "user_id"),)

    like_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tweet_id: Mapped[int] = mapped_column(ForeignKey(column="tweets.tweet_id"))
    user_id: Mapped[int] = mapped_column(ForeignKey(column="users.id"))

    tweet: Mapped[list["Tweets"]] = relationship(
        "Tweets", back_populates="likes"
    )
    user: Mapped[list["Users"]] = relationship("Users", back_populates="likes")

    def __repr__(self):
        return (
            f"Like: like_id={self.like_id}, "
            f"tweet_id={self.tweet_id}, "
            f"user_id={self.user_id}"
        )
