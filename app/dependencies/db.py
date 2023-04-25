from typing import Generator

from db.base import SessionLocal


def get_session() -> Generator:
    try:
        session = SessionLocal()
        yield session
    finally:
        session.close()
