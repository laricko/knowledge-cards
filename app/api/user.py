from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from schemas.user import User, UserIn
from dependencies.db import get_session
from dependencies.auth import get_current_user
from crud import user as crud
from services.send_verification_email import send_verification_email


user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.get("/", response_model=User)
async def self_user(user: User = Depends(get_current_user)):
    return user


@user_router.patch("/", response_model=User)
async def patch_self_user(
    data: UserIn,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    exists, field = crud.check_username_or_email_exists(
        user.id, session, **data.dict(exclude_unset=True)
    )
    if exists:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"{field} already exists")
    updated_user = crud.update_user(data, user.id, session)
    if user.email != updated_user["email"]:
        send_verification_email(user.id, session)
    return updated_user
