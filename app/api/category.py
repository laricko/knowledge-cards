from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from crud import category as crud
from dependencies.auth import get_current_user_is_verified
from dependencies.db import get_session
from schemas.category import Category, CategoryIn, CategoryOrdering, CategoryUpdate
from schemas.response import DetailResponse
from schemas.user import User

category_router = APIRouter(
    prefix="/category",
    tags=["category"],
    dependencies=[Depends(get_current_user_is_verified)],
)


@category_router.get("/my", response_model=list[Category])
async def my_categories(
    title: str | None = None,
    ordering: CategoryOrdering = CategoryOrdering.id,
    skip: int = 0,
    limit: int = 20,
    user: User = Depends(get_current_user_is_verified),
    session: Session = Depends(get_session),
):
    categories = crud.get_category_for_user(
        user.id, session, title=title, ordering=ordering, limit=limit, skip=skip
    )
    return categories


@category_router.post("/", response_model=Category, status_code=status.HTTP_201_CREATED)
async def create_category(
    data: CategoryIn,
    user: User = Depends(get_current_user_is_verified),
    session: Session = Depends(get_session),
):
    category = crud.create_category(user.id, data, session)
    return category


@category_router.delete("/{id}", response_model=DetailResponse)
async def delete_category(id: int, session: Session = Depends(get_session)):
    crud.delete_category(id, session)
    return DetailResponse(detail="success")


@category_router.patch("/{id}", response_model=Category)
async def update_category(
    id: int, data: CategoryUpdate, session: Session = Depends(get_session)
):
    category = crud.update_category(id, data, session)
    return category


@category_router.get("/system", response_model=list[Category])
async def system_categories(session: Session = Depends(get_session)):
    categories = crud.get_system_categories(session)
    return categories


@category_router.post(
    "/{id}/add-system",
    response_model=DetailResponse,
)
async def add_system_category(
    id: int,
    user: User = Depends(get_current_user_is_verified),
    session: Session = Depends(get_session),
):
    crud.add_system_category(id, user.id, session)
    return DetailResponse(detail="success")


@category_router.post("/{id}/remove-system", response_model=DetailResponse)
async def remove_system_category(
    id: int,
    user: User = Depends(get_current_user_is_verified),
    session: Session = Depends(get_session),
):
    crud.remove_system_category(id, user.id, session)
    return DetailResponse(detail="success")
