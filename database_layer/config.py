from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(extra='ignore', env_file=('.env.dev', '.env'))

    DB: str = 'sqlite'
    DB_DRIVER: str = 'aiosqlite'
    DB_USER: Optional[str] = None
    DB_PASS: Optional[str] = None
    DB_HOST: Optional[str] = None
    DB_PORT: Optional[int] = None
    DB_NAME: Optional[str] = 'database.sqlite'
    DB_POOL_SIZE: Optional[int] = None

    ECHO: bool = False

    @property
    def url(self):
        db = self.DB
        driver = self.DB_DRIVER
        db_name = self.DB_NAME
        user = self.DB_USER
        password = self.DB_PASS
        host = self.DB_HOST
        port = self.DB_PORT
        return f"{db}+{driver}://{user}:{password}@{host}:{port}/{db_name}"

    @property
    def sqlite_url(self):
        db = self.DB
        driver = self.DB_DRIVER
        db_name = self.DB_NAME
        return f"{db}+{driver}:///{db_name}.sqlite"

    @property
    def alembic_url(self):
        db = self.DB
        db_name = self.DB_NAME
        user = self.DB_USER
        password = self.DB_PASS
        host = self.DB_HOST
        port = self.DB_PORT
        return f"{db}://{user}:{password}@{host}:{port}/{db_name}"


settings: DatabaseSettings = DatabaseSettings()
