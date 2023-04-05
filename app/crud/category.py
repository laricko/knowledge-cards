from sqlalchemy.orm import Session
from sqlalchemy import insert, literal_column, select, update, delete, or_, desc

from db.card import category, related_system_categories_with_user
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
        .where(
            *title_filter,
            or_(
                category.c.user_id == user_id,
                category.c.id.in_(
                    select(related_system_categories_with_user.c.category_id).where(
                        related_system_categories_with_user.c.user_id == user_id
                    )
                ),
            ),
        )
        .order_by(desc(category.c.user_id), get_ordering(category, ordering))
        .limit(limit)
        .offset(skip)
    )
    cur = session.execute(query)
    return cur.mappings().all()


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


def get_system_categories(session: Session) -> list[dict]:
    query = select(category).where(category.c.user_id == None)
    cur = session.execute(query)
    return cur.mappings().all()


def add_system_category(category_id: int, user_id: int, session: Session) -> None:
    query = insert(related_system_categories_with_user).values(
        category_id=category_id, user_id=user_id
    )
    session.execute(query)
    session.commit()
    return


def remove_system_category(category_id: int, user_id: int, session: Session) -> None:
    table_c = related_system_categories_with_user.c
    query = delete(related_system_categories_with_user).where(
        table_c.user_id == user_id, table_c.category_id == category_id
    )
    session.execute(query)
    session.commit()
    return
