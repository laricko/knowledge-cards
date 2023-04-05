from fastapi import APIRouter

from api.auth import auth_router, verification_router
from api.user import user_router
from api.card import card_router
from api.category import category_router
from api.suggestion import suggest_router


api_router = APIRouter(prefix="/api")
api_router.include_router(auth_router)
api_router.include_router(verification_router)
api_router.include_router(user_router)
api_router.include_router(card_router)
api_router.include_router(category_router)
api_router.include_router(suggest_router)
