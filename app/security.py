from datetime import datetime, timedelta

from jose import jwt
from jose.exceptions import JWTError
from passlib.context import CryptContext
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from config import get_settings


settings = get_settings()
password_context = CryptContext("bcrypt", deprecated="auto")
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


def hash_password(password: str) -> str:
    return password_context.hash(password)


def verify_passwrod(password: str, hash: str) -> bool:
    return password_context.verify(password, hash)


def create_access_token(data: dict) -> str:
    to_encode = dict(data)
    to_encode.update(
        {"exp": datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)}
    )
    token = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)
    return token


def decode_access_token(token: str):
    try:
        return jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except JWTError:
        return None
