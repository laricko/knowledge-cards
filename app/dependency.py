from typing import Generator

from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session

from schemas.user import User
from db.base import SessionLocal
from security import JWTBearer, invalid_token_exception
from crud import user as crud


def get_session() -> Generator:
    try:
        session = SessionLocal()
        yield session
    finally:
        session.close()


async def get_current_user(
    data: str = Depends(JWTBearer()), session: Session = Depends(get_session)
) -> User:
    user = crud.get_user_by_email(data.get("sub"), session)
    if not user:
        raise invalid_token_exception
    return User.parse_obj(user)


async def get_current_user_is_verified(
    user: User = Depends(get_current_user),
) -> User:
    if not user.verified:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "You must verify your email")
    return user
