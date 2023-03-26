from typing import Generator

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException, status, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from schemas.user import User
from security import decode_access_token
from db.base import SessionLocal
from db.user import user as user_db


def get_session() -> Generator:
    try:
        session = SessionLocal()
        yield session
    finally:
        session.close()


invalid_token_exception = HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid token")


class JWTBearer(HTTPBearer):
    def __init__(self, *args, auto_eror: bool = True, **kwargs):
        super().__init__(*args, auto_error=auto_eror, **kwargs)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        credentials = await super().__call__(request)
        if not credentials:
            raise invalid_token_exception
        else:
            data = decode_access_token(credentials.credentials)
            if data is None:
                raise invalid_token_exception
            return data


async def get_current_user(
    data: str = Depends(JWTBearer()), session: Session = Depends(get_session)
) -> User:
    query = select(user_db).where(user_db.c.email == data.get("sub"))
    user = session.execute(query).first()
    if not user:
        raise invalid_token_exception
    return User.parse_obj(user._asdict())


async def get_current_user_is_verified(
    user: User = Depends(get_current_user),
) -> User:
    if not user.verified:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "You must verify your email")
    return user
