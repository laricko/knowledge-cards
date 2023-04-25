from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from crud import user as crud
from schemas.user import User
from security import JWTBearer, invalid_token_exception

from .db import get_session


async def get_current_user(
    data: str = Depends(JWTBearer()), session: Session = Depends(get_session)
) -> User:
    user = crud.get_user_by_email(data.get("sub"), session)
    if not user:
        raise invalid_token_exception
    return user


async def get_current_user_is_verified(
    user: User = Depends(get_current_user),
) -> User:
    if user.verified:
        return user
    raise HTTPException(status.HTTP_403_FORBIDDEN, "You must verify your email")
