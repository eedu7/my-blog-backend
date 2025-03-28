from enum import StrEnum

from pathlib import Path
from pydantic_settings import BaseSettings

from pydantic import PostgresDsn


class EnvironmentType(StrEnum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TEST = "test"


class BaseConfig(BaseSettings):
    class Config:
        case_sensitive = True
        env_file = Path(__file__).resolve().parent.parent / ".env"
        env_file_encoding = "utf-8"


class Config(BaseConfig):
    DEBUG: int = 0
    DEFAULT_LOCALE: str = "en_US"
    ENVIRONMENT: str = EnvironmentType.DEVELOPMENT
    POSTGRES_URL: PostgresDsn | str = (
        "postgresql+asyncpg://user:password@127.0.0.1:5432/db-name"
    )
    TEST_POSTGRES_URL: PostgresDsn | str = (
        "postgresql+asyncpg://user:password@127.0.0.1:5432/db-name"
    )
    JWT_SECRET_KEY: str = "super-secret-key"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60 * 24
    SHOW_SQL_ALCHEMY_QUERIES: int
    RELEASE_VERSION: str = "1.0.0"


config: Config = Config()
