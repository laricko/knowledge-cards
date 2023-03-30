from datetime import datetime

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int
    username: str | None
    email: EmailStr
    first_name: str | None
    last_name: str | None
    created: datetime
    updated: datetime | None
    verified: bool


class UserIn(BaseModel):
    username: str | None
    email: EmailStr | None
    first_name: str | None
    last_name: str | None
