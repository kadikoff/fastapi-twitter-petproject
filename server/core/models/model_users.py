from typing import TYPE_CHECKING

from sqlalchemy import String, Table, Column, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .model_base import Base

if TYPE_CHECKING:
    from .model_likes import Likes
    from .model_tweets import Tweets


followers_association_table = Table(
    "followers_association",
    Base.metadata,
    Column("follower_id", ForeignKey("users.id"), primary_key=True),
    Column("following_id", ForeignKey("users.id"), primary_key=True),
    UniqueConstraint("follower_id", "following_id", name="unique_user_followers"),
)


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30))
    api_key: Mapped[str] = mapped_column(String(10), unique=True)

    tweets: Mapped[list["Tweets"]] = relationship(
        "Tweets", back_populates="user", cascade="all, delete-orphan"
    )
    likes: Mapped[list["Likes"]] = relationship("Likes", back_populates="user")

    followers: Mapped[list["Users"]] = relationship(
        "Users",
        secondary=followers_association_table,
        primaryjoin=(followers_association_table.c.following_id == id),
        secondaryjoin=(followers_association_table.c.follower_id == id),
        back_populates="following",
    )
    following: Mapped[list["Users"]] = relationship(
        "Users",
        secondary=followers_association_table,
        primaryjoin=(followers_association_table.c.follower_id == id),
        secondaryjoin=(followers_association_table.c.following_id == id),
        back_populates="followers",
        lazy="selectin",
    )

    def __repr__(self):
        return f"User: id={self.id}, name={self.name}, api_key={self.api_key}"
