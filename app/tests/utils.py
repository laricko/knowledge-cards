from sqlalchemy.orm import Session
from sqlalchemy import insert, literal_column, text

from db.user import user as user_db
from security import hash_password, create_access_token

TEST_USER_PASSWORD = "string"


def create_user(db: Session, verified: bool) -> dict:
    if verified:
        username = "username"
        email = "user@string.com"
    else:
        username = "dumb_username"
        email = "dumb_email@string.com"
    query = (
        insert(user_db)
        .values(
            username=username,
            email=email,
            password=hash_password(TEST_USER_PASSWORD),
            first_name="firstName",
            last_name="lastName",
            verified=verified,
        )
        .returning(literal_column("*"))
    )
    cur = db.execute(query)
    db.commit()
    return cur.first()._asdict()


def get_auth_token(user: dict) -> str:
    return create_access_token(user["email"])
