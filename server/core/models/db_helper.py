from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from server.core.config import settings


class DatabaseHelper:
    """Вспомогательный класс для работы с
    асинхронной базой данных

    Обеспечивает управления подключениями к БД и сессиями
    SQLAlchemy в асинхронном режиме.
    """

    def __init__(self, url: str, echo: bool = False):
        """Инициализирует асинхронное подключение к БД
        и фабрику сессий
        """
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def session_dependency(self) -> AsyncGenerator[AsyncSession, None]:
        """Генератор асинхронных сессий для
        использования в FastAPI Depends
        """
        async with self.session_factory() as session:
            yield session
            await session.close()


db_helper = DatabaseHelper(
    url=settings.db.url,
    echo=settings.db.db_echo,
)
