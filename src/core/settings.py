import os
import secrets
from pathlib import Path

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class DevSettings(BaseSettings):
    PG_DSN: PostgresDsn
    SQLALCHEMY_POOL_SIZE: int = 20
    SQLALCHEMY_POOL_RECYCLE: int = 1200
    SQLALCHEMY_POOL_TIMEOUT: int = 5
    SQLALCHEMY_MAX_OVERFLOW: int = 10

    JWT_SECRET_KEY: str = secrets.token_urlsafe(32)
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE: int = 60 * 15
    REFRESH_TOKEN_EXPIRE: int = 60 * 60 * 24 * 30

    model_config = SettingsConfigDict(env_file=os.path.join(BASE_DIR, ".env"), env_file_encoding="utf-8")


dev_settings = DevSettings()
