from sqlalchemy.orm import Session

from utils.send_email import send_email
from crud import user as crud


def send_verification_email(user_id, session: Session) -> None:
    token = crud.create_verification_token(user_id, session)
    subject = "Knowledge cards: Verification email"
    body = (
        f"http://localhost:8000/api/verify-email?token={token['value']}"  # must be html
    )
    send_email(subject, body)
