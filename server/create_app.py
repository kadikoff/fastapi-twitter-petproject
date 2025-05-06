import logging
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from fastapi import FastAPI

from server.api.routes import router
from server.core.config import settings
from server.core.middlewares import register_middlewares
from server.core.models import db_helper
from server.error_handlers import register_errors_handlers
from server.utils.create_mock_data import create_mock_data

logging.basicConfig(level=logging.INFO, format=settings.logging.log_format)

log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    """Контекстный менеджер жизненного цикла приложения FastAPI

    Выполняет:
    1. Инициализацию тестовых данных при старте (create_mock_data)
    2. Корректное освобождение ресурсов БД при завершении
    """

    await create_mock_data()
    yield
    await db_helper.engine.dispose()


def create_app() -> FastAPI:
    """Создания экземпляра приложения FastAPI"""

    app = FastAPI(
        default_response_class=settings.api.default_response_class,
        lifespan=lifespan,
        title=settings.api.docs_title,
        description=settings.api.docs_description,
    )

    app.include_router(router=router)
    register_errors_handlers(app)
    register_middlewares(app)

    return app
