from fastapi import APIRouter

from api.auth import auth_router, verification_router
from api.user import user_router


api_router = APIRouter(prefix="/api")
api_router.include_router(auth_router)
api_router.include_router(verification_router)
api_router.include_router(user_router)
