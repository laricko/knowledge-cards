from sqlalchemy.orm import Session
from sqlalchemy import insert, literal_column, select, update, delete

from db.card import category
from schemas.category import CategoryIn
from utils.get_ordering import get_ordering


def create_category(user_id: int, data: CategoryIn, session: Session) -> dict:
    query = (
        insert(category)
        .values(user_id=user_id, **data.dict())
        .returning(literal_column("*"))
    )
    cur = session.execute(query)
    session.commit()
    return cur.first()._asdict()


def get_category_for_user(
    user_id: int,
    session: Session,
    *,
    title: str | None,
    ordering: str,
    limit: int,
    skip: int,
) -> list[dict]:
    title_filter = [category.c.title.ilike(f"%{title}%")] if title else []
    query = (
        select(category)
        .where(category.c.user_id == user_id, *title_filter)
        .order_by(get_ordering(category, ordering))
        .limit(limit)
        .offset(skip)
    )
    cur = session.execute(query)
    rows = cur.mappings().all()
    return rows


def update_category(category_id: int, data: CategoryIn, session: Session) -> dict:
    query = (
        update(category)
        .values(**data.dict(exclude_unset=True))
        .where(category.c.id == category_id)
        .returning(literal_column("*"))
    )
    cur = session.execute(query)
    session.commit()
    return cur.first()._asdict()


def delete_category(category_id: int, session: Session) -> None:
    query = delete(category).where(category.c.id == category_id)
    session.execute(query)
    session.commit()
    return
