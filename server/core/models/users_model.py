from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base_model import Base


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    api_key: Mapped[str] = mapped_column(String(30), nullable=False)

    def __repr__(self):
        return f"User: id={self.id}, name={self.name}, api_key={self.api_key}"
