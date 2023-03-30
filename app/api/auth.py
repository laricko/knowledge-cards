from fastapi import APIRouter, HTTPException, status, Depends, BackgroundTasks
from pydantic import BaseModel, validator, EmailStr
from sqlalchemy import insert, select, update
from sqlalchemy.orm import Session

from schemas.user import User
from schemas.response import DetailResponse
from dependency import get_session
from db.user import user as user_db, token as token_db
from security import hash_password, verify_passwrod, create_access_token
from services.create_verification_token_and_send_email import (
    create_verification_token_and_send_email,
)


auth_router = APIRouter(prefix="/auth", tags=["auth"])


class RegisterData(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str

    @validator("confirm_password")
    def passwords_match(cls, v, values, **kwargs):
        if v != values["password"]:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "passwords do not match")
        return v


@auth_router.post(
    "/register",
    response_model=RegisterData,
    response_model_exclude=("confirm_password",),
)
async def register(
    background_tasks: BackgroundTasks,
    data: RegisterData,
    session: Session = Depends(get_session),
):
    query_to_insert_user = (
        insert(user_db)
        .values(email=data.email, password=hash_password(data.password))
        .returning(user_db.c.id)
    )
    row = session.execute(query_to_insert_user)
    session.commit()
    user_id = row.first().id
    background_tasks.add_task(
        create_verification_token_and_send_email(user_id, session)
    )
    return data


class LoginData(BaseModel):
    email: EmailStr
    password: str


class UserLoginResponse(User):
    token: str


@auth_router.post("/login", response_model=UserLoginResponse)
async def login(data: LoginData, session: Session = Depends(get_session)):
    exc = HTTPException(
        status.HTTP_403_FORBIDDEN, "There is no user with such email and password"
    )
    query = select(user_db).where(user_db.c.email == data.email)
    user = session.execute(query).first()
    if not user:
        raise exc
    password_match = verify_passwrod(data.password, user.password)
    if not password_match:
        raise exc
    response = user._asdict()
    response["token"] = create_access_token({"sub": data.email})
    return response


verification_router = APIRouter(tags=["verification"])


@verification_router.get("/verify-email", response_model=DetailResponse)
async def verify_email(token: str, session: Session = Depends(get_session)):
    query_to_get_token = select(token_db).where(token_db.c.value == token)
    token_instance = session.execute(query_to_get_token).first()
    if not token_instance:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "token not valid")
    query_to_get_user = select(user_db).where(user_db.c.id == token_instance.user_id)
    user = session.execute(query_to_get_user).first()
    if user.verified:
        return {"detail": "success"}
    query_to_make_user_verified = (
        update(user_db)
        .where(user_db.c.id == token_instance.user_id)
        .values(verified=True)
    )
    session.execute(query_to_make_user_verified)
    session.commit()
    return {"detail": "success"}
