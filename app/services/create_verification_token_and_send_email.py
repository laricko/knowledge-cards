from uuid import uuid4

from sqlalchemy import insert
from sqlalchemy.orm import Session

from db.user import token

from utils.send_email import send_email


def create_verification_token_and_send_email(
    user_id: int, session: Session
) -> None:
    random_token = str(uuid4())
    subject = "subject"
    body = f"http://localhost:8000/api/verify-email?token={random_token}"
    query = insert(token).values(user_id=user_id, value=random_token)
    session.execute(query)
    session.commit()
    send_email(subject, body)
