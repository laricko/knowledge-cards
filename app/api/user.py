from datetime import datetime

from fastapi import Depends, APIRouter, HTTPException, status, BackgroundTasks
from sqlalchemy import update, literal_column, select
from sqlalchemy.orm import Session

from dependency import get_session
from db.user import user as user_db
from schemas.user import User, UserIn
from dependency import get_current_user
from services.create_verification_token_and_send_email import (
    create_verification_token_and_send_email,
)


user_router = APIRouter(prefix="/self-user", tags=["user"])


@user_router.get("/", response_model=User)
async def self_user(user: User = Depends(get_current_user)):
    return user


def check_username_or_email_exists(user_id: int, session: Session, **kwargs) -> None:
    fields_to_check = {"username": kwargs.get("username"), "email": kwargs.get("email")}
    filtered_fields_to_check = {
        k: v for k, v in fields_to_check.items() if v is not None
    }
    for key, value in filtered_fields_to_check.items():
        column = getattr(user_db.c, key)
        query = select(column).where(column == value, user_db.c.id != user_id)
        row = session.execute(query).first()
        if row:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, f"{key} already exists")


@user_router.patch("/", response_model=User)
async def patch_self_user(
    data: UserIn,
    background_tasks: BackgroundTasks,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    data = data.dict(exclude_unset=True)
    check_username_or_email_exists(user.id, session, **data)
    if data.get("email") != user.email:
        background_tasks.add_task(
            create_verification_token_and_send_email(user.id, session)
        )
        # NOTE: need make user unverified? or create another table for emails?
    data["updated"] = datetime.now()
    query = (
        update(user_db)
        .values(data)
        .where(user_db.c.id == user.id)
        .returning(literal_column("*"))
    )
    r = session.execute(query)
    session.commit()
    return r.first()._asdict()
