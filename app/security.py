from datetime import datetime, timedelta

from passlib.context import CryptContext
from jose.exceptions import JWTError
from jose import jwt

from config import get_settings


settings = get_settings()
password_context = CryptContext("bcrypt", deprecated="auto")


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