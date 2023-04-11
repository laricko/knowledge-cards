from typing import Generator
import os

from fastapi.testclient import TestClient
from fastapi import FastAPI
from pytest import fixture
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import alembic
from alembic.config import Config

from dependencies.auth import get_session
from config import get_settings

from .utils import create_user


def get_session_to_test_db() -> Generator:
    settings = get_settings()
    database_url = f"{settings.DATABASE_URL}_test"
    engine = create_engine(database_url, pool_pre_ping=True)
    SessionLocal = sessionmaker(engine)
    try:
        session = SessionLocal()
        yield session
    finally:
        session.close()


@fixture(scope="session")
def db() -> Generator:
    return get_session_to_test_db().__next__()


@fixture(scope="session")
def apply_migrations():
    os.environ["TESTING"] = "1"
    config = Config("alembic.ini")
    alembic.command.upgrade(config, "head")
    yield
    # alembic.command.downgrade(config, "base")


@fixture(scope="session")
def app(apply_migrations) -> FastAPI:
    from main import create_application

    application = create_application()
    application.dependency_overrides[get_session] = get_session_to_test_db
    return application


@fixture(scope="session")
def client(app) -> TestClient:
    return TestClient(app, "http://localhost:8000/api")


@fixture(scope="session")
def unverified_user(db: Session) -> dict:
    return create_user(db, False)


@fixture(scope="session")
def user(db: Session) -> dict:
    return create_user(db, True)
