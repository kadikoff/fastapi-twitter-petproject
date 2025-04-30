import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_PROJECT_DIR = Path(__file__).parent.parent.parent  # /project
BASE_MEDIAS_DIR = BASE_PROJECT_DIR / "server/medias"  # /project/server/medias

MEDIAS_ALLOWED_EXT = {".jpg", ".jpeg", ".png"}


class DbSettings(BaseSettings):
    db_user: str
    db_pass: str
    db_host: str
    db_host_local: str
    db_port: int
    db_name: str
    db_echo: bool = True

    @property
    def url(self):
        return (
            f"postgresql+asyncpg"
            f"://{self.db_user}:{self.db_pass}@{self.db_host}"
            f":{self.db_port}/{self.db_name}"
        )

    @property
    def url_local(self):
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
    db: DbSettings = DbSettings()


settings = Settings()
