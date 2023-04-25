from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from crud import user as crud
from dependencies.db import get_session
from schemas.auth import LoginData, RegisterData, UserLoginResponse
from schemas.response import DetailResponse
from security import create_access_token, verify_passwrod
from services.send_verification_email import send_verification_email

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post(
    "/register",
    response_model=RegisterData,
    response_model_exclude=("confirm_password",),
    status_code=status.HTTP_201_CREATED,
    name="auth:register",
)
async def register(
    data: RegisterData,
    session: Session = Depends(get_session),
):
    user_exists = crud.get_user_by_email(data.email, session)
    if user_exists:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "email already exists")
    user = crud.create_user(data, session)
    send_verification_email(user.id, session)
    return data


@auth_router.post("/login", response_model=UserLoginResponse, name="auth:login")
async def login(data: LoginData, session: Session = Depends(get_session)):
    exc = HTTPException(
        status.HTTP_403_FORBIDDEN, "There is no user with such email and password"
    )
    user = crud.get_user_by_email(data.email, session, get_password=True)

    if not user:
        raise exc

    password_match = verify_passwrod(data.password, user.password)
    if not password_match:
        raise exc

    return UserLoginResponse(token=create_access_token(data.email), **user.dict())


verification_router = APIRouter(tags=["verification"])


@verification_router.get(
    "/verify-email", response_model=DetailResponse, name="verification:verify"
)
async def verify_email(token: str, session: Session = Depends(get_session)):
    verification_token = crud.get_verification_token(token, session)
    if not verification_token:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "token not valid")
    crud.make_user_verified(verification_token.user_id, session)
    return {"detail": "success"}
