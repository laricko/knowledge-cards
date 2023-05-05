from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from crud import user as crud
from dependencies.db import get_session
from schemas.response import DetailResponse

verification_router = APIRouter(tags=["verification"])


@verification_router.get(
    "/verify-email", response_model=DetailResponse, name="verification:verify"
)
async def verify_email(token: str, session: Session = Depends(get_session)):
    verification_token = crud.get_verification_token(token, session)
    if not verification_token:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "token not valid")
    crud.make_user_verified(verification_token.user_id, session)
    return DetailResponse(detail="success")
