from sqlalchemy.orm import Session

from crud import user as crud
from schemas.user import User
from utils.send_email import send_email


def send_verification_email(user: User, session: Session) -> None:
    token = crud.create_verification_token(user.id, session)
    subject = "Knowledge cards: Verification email"
    body = f"http://localhost:8000/api/verify-email?token={token.value}"  # must be html
    send_email(user.email, subject, body)
