from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .model_base import Base

if TYPE_CHECKING:
    from .model_tweets import Tweets


class Medias(Base):
    __tablename__ = "medias"

    media_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    media_path: Mapped[str]
    tweet_id: Mapped[int | None] = mapped_column(
        ForeignKey(column="tweets.tweet_id")
    )

    tweet: Mapped[list["Tweets"]] = relationship(
        "Tweets", back_populates="medias"
    )

    def __repr__(self):
        return (
            f"Media: media_id={self.media_id}, "
            f"media_path={self.media_path}, "
            f"tweet_id={self.tweet_id}"
        )
