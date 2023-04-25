from fastapi import HTTPException, status
from pydantic import BaseModel, EmailStr, validator

from .user import User


class RegisterData(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str

    @validator("confirm_password")
    def passwords_match(cls, v, values, **kwargs):
        if v != values["password"]:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "passwords do not match")
        return v


class LoginData(BaseModel):
    email: EmailStr
    password: str


class UserLoginResponse(User):
    token: str
