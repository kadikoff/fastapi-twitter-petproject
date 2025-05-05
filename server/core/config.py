import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Путь до корневой папки проекта
BASE_PROJECT_DIR = Path(__file__).parent.parent.parent  # /project

# Путь до директории хранения медиа-файлов
# При изменении пути до BASE_MEDIA_DIR следует также изменить его
# в docker-compose.yml в volumes к nginx и server
BASE_MEDIAS_DIR = BASE_PROJECT_DIR / "server/medias"  # /project/server/medias

# Расширения медиа-файлов, допустимые к загрузке вместе с твитами
MEDIAS_ALLOWED_EXT = {".jpg", ".jpeg", ".png"}


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
    db_echo: bool = True

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

    model_config = SettingsConfigDict(
        env_file=os.path.join(BASE_PROJECT_DIR, ".env"),
        env_file_encoding="utf-8",
    )


class Settings(BaseSettings):
    """Корневая конфигурация приложения"""

    db: DbSettings = DbSettings()


settings = Settings()
