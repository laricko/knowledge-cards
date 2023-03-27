from fastapi import Depends, APIRouter, status
from sqlalchemy.orm import Session

from dependency import get_current_user_is_verified, get_session
from schemas.user import User
from schemas.card import CardIn, Card, CardsOrdering, CardUpdate
from crud import card as crud


card_router = APIRouter(
    prefix="/card", tags=["card"], dependencies=[Depends(get_current_user_is_verified)]
)


@card_router.get("/my", response_model=list[Card])
async def my_cards(
    ordering: CardsOrdering = CardsOrdering.id,
    title: str | None = None,
    category_id: int | None = None,
    limit: int = 20,
    offset: int = 0,
    user: User = Depends(get_current_user_is_verified),
    session: Session = Depends(get_session),
):
    cards = crud.get_cards_by_user(
        user.id,
        session,
        ordering=ordering,
        title=title,
        category_id=category_id,
        limit=limit,
        offset=offset,
    )
    return cards


@card_router.post("/", response_model=Card, status_code=status.HTTP_201_CREATED)
async def create_card(
    data: CardIn,
    user: User = Depends(get_current_user_is_verified),
    session: Session = Depends(get_session),
):
    card = crud.create_card(user.id, data, session)
    return card


@card_router.patch("/{id}", response_model=Card)
async def update_card(id: int, data: CardUpdate, session: Session = Depends(get_session)):
    card = crud.update_card(id, data, session)
    return card


@card_router.delete("/{id}")
async def delete_card(id: int, session: Session = Depends(get_session)):
    crud.delete_card(id, session)
    return {"detail": "success"}
