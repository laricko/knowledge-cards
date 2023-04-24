from datetime import datetime

from pydantic import parse_obj_as
from sqlalchemy.orm import Session
from sqlalchemy import insert, literal_column, select, update, delete

from utils.get_ordering import get_ordering
from db.card import card
from schemas.card import CardIn, CardUpdate, Card


def get_cards_by_user(
    user_id: int,
    session: Session,
    *,
    title: str | None,
    category_id: int,
    ordering: str | None,
    limit: int,
    skip: int,
) -> list[Card]:
    filters = []
    if title:
        filters.append(card.c.title.ilike(f"%{title}%"))
    if category_id:
        filters.append(card.c.category_id == category_id)
    query = (
        select(card)
        .filter(*filters, card.c.user_id == user_id)
        .order_by(get_ordering(card, ordering))
        .limit(limit)
        .offset(skip)
    )
    cur = session.execute(query)
    return parse_obj_as(list[Card], cur.mappings().all())


def create_card(user_id: int, data: CardIn, session: Session) -> Card:
    query = (
        insert(card)
        .values(user_id=user_id, **data.dict())
        .returning(literal_column("*"))
    )
    cur = session.execute(query)
    session.commit()
    return Card.parse_obj(cur.first()._asdict())


def update_card(id: int, data: CardUpdate, session: Session) -> Card:
    data_as_dict = data.dict(exclude_unset=True)
    data_as_dict["updated"] = datetime.now()
    query = (
        update(card)
        .values(**data_as_dict)
        .where(card.c.id == id)
        .returning(literal_column("*"))
    )
    cur = session.execute(query)
    session.commit()
    return Card.parse_obj(cur.first()._asdict())


def delete_card(id: int, session: Session) -> None:
    query = delete(card).where(card.c.id == id)
    session.execute(query)
    session.commit()
    return
