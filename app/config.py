from os import environ
from functools import lru_cache

from starlette.config import Config
from pydantic import BaseSettings, PostgresDsn


config = Config("development.env")


class SystemCategories(BaseSettings):
    english = "Language English"


class Settings(BaseSettings):
    PROJECT_TITLE = config("PROJECT_TITLE", str, "")
    SITE_PORT = config("SITE_PORT", int)
    SITE_HOST = config("SITE_HOST", str)

    _POSTGRES_DB = config("POSTGRES_DB")
    _POSTGRES_USER = config("POSTGRES_USER")
    _POSTGRES_PASSWORD = config("POSTGRES_PASSWORD")

    DATABASE_URL: PostgresDsn = (
        f"postgresql://{_POSTGRES_USER}:{_POSTGRES_PASSWORD}@db:5432/{_POSTGRES_DB}"
    )

    environ["DATABASE_URL"] = DATABASE_URL

    JWT_EXPIRE_MINUTES = config("JWT_EXPIRE_MINUTES", int)
    ALGORITHM = config("ALGORITHM")
    SECRET_KEY = config("SECRET_KEY")

    OPENAI_API_KEY = config("OPENAI_API_KEY", str)

    system_categories = ["Language English", "Language Russian"]


@lru_cache()
def get_settings() -> BaseSettings:
    return Settings()
