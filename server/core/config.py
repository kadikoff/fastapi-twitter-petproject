import logging
from pathlib import Path
from typing import ClassVar, Type

from dotenv import load_dotenv
from fastapi.openapi.models import Response
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel
from pydantic_settings import BaseSettings

# Путь до корневой папки проекта
BASE_PROJECT_DIR = Path(__file__).parent.parent.parent  # /project

# Путь до директории хранения медиа-файлов
# При изменении пути до BASE_MEDIA_DIR следует также изменить его
# в docker-compose.yml в volumes к nginx и server
BASE_MEDIAS_DIR = BASE_PROJECT_DIR / "server/medias"  # /project/server/medias

# Расширения медиа-файлов, допустимые к загрузке вместе с твитами
MEDIAS_ALLOWED_EXT = {".jpg", ".jpeg", ".png"}

LOG_DEFAULT_FORMAT = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d "
    "%(levelname)-7s - %(message)s"
)

API_DOCS_TITLE = "Twitter-clone API Documentation"
API_DOCS_DESCRIPTION = (
    "API-документация для Pet-проекта аналога Twitter. "
    "В целях тестирования для авторизации используется "
    "один из двух доступных api_key: test или dev"
)

load_dotenv()


class FastApiConfig(BaseModel):
    """Настройки для приложения FastAPI"""

    default_response_class: ClassVar[Type[Response]] = ORJSONResponse
    docs_title: str = API_DOCS_TITLE
    docs_description: str = API_DOCS_DESCRIPTION


class RunConfig(BaseModel):
    """Настройки для Uvicorn"""

    host: str = "0.0.0.0"
    port: int = 8000
    app: str = "main:app"
    reload: bool = True


class LoggingConfig(BaseModel):
    """Настройки для логгирования"""

    log_level: int = logging.DEBUG
    log_format: str = LOG_DEFAULT_FORMAT


class DbSettings(BaseSettings):
    """Настройки подключение к PostgreSQL базе данных

    Считывает параметры подключения из .env файла.
    Предоставляет свойства для формирования DSN строк подключения.
    """

    db_user: str
    db_pass: str
    db_host: str
    db_host_local: str
    db_port: int
    db_name: str
    db_echo: bool = False

    @property
    def url(self):
        """Формирует DSN строку для production подключения"""
        return (
            f"postgresql+asyncpg"
            f"://{self.db_user}:{self.db_pass}@{self.db_host}"
            f":{self.db_port}/{self.db_name}"
        )

    @property
    def url_local(self):
        """Формирует DSN строку для локального подключения"""
        return (
            f"postgresql+asyncpg"
            f"://{self.db_user}:{self.db_pass}@{self.db_host_local}"
            f":{self.db_port}/{self.db_name}"
        )


class Settings(BaseSettings):
    """Корневая конфигурация приложения"""

    api: FastApiConfig = FastApiConfig()
    run: RunConfig = RunConfig()
    db: DbSettings = DbSettings()
    logging: LoggingConfig = LoggingConfig()


settings = Settings()
