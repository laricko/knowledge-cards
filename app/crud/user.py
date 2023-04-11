from uuid import uuid4
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import insert, select, update, literal_column

from db.user import user as user_db, token as token_db
from security import hash_password
from schemas.auth import RegisterData
from schemas.user import UserIn


def create_user(data: RegisterData, session: Session) -> dict:
    query = (
        insert(user_db)
        .values(email=data.email, password=hash_password(data.password))
        .returning(user_db.c.id)
    )
    cur = session.execute(query)
    session.commit()
    return cur.first()._asdict()


def get_user_by_email(email: str, session: Session) -> dict | None:
    query = select(user_db).where(user_db.c.email == email)
    cur = session.execute(query)
    row = cur.first()
    return row and row._asdict() or None


def get_verification_token(token: str, session: Session) -> dict | None:
    query = select(token_db).where(token_db.c.value == token)
    cur = session.execute(query)
    row = cur.first()
    return row and row._asdict() or None


def make_user_verified(user_id: int, session: Session) -> None:
    query = select(user_db).where(user_db.c.id == user_id)
    cur = session.execute(query)
    row = cur.first()
    user = row._asdict()
    if user["verified"]:
        return
    query = update(user_db).where(user_db.c.id == user_id).values(verified=True)
    session.execute(query)
    session.commit()
    return


def create_verification_token(user_id: int, session: Session) -> dict:
    random_token = str(uuid4())
    query = (
        insert(token_db)
        .values(user_id=user_id, value=random_token)
        .returning(token_db.c.value)
    )
    cur = session.execute(query)
    session.commit()
    return cur.first()._asdict()


def update_user(data: UserIn, user_id: int, session: Session) -> dict:
    data = data.dict(exclude_unset=True) # here partial update only
    data["updated"] = datetime.now()
    query = (
        update(user_db)
        .values(data)
        .where(user_db.c.id == user_id)
        .returning(literal_column("*"))
    )
    cur = session.execute(query)
    session.commit()
    return cur.first()._asdict()


def check_username_or_email_exists(
    user_id: int, session: Session, **kwargs
) -> tuple[bool, str | None]:
    fields_to_check = {"username": kwargs.get("username"), "email": kwargs.get("email")}
    filtered_fields_to_check = {
        k: v for k, v in fields_to_check.items() if v is not None
    }
    for key, value in filtered_fields_to_check.items():
        column = getattr(user_db.c, key)
        query = select(column).where(column == value, user_db.c.id != user_id)
        row = session.execute(query).first()
        if row:
            return True, key
    return False, None
