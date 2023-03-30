from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class CategoryOrdering(str, Enum):
    id = "id"
    d_id = "-id"
    title = "title"
    d_title = "-title"
    created = "created"
    d_created = "-created"


class CategoryIn(BaseModel):
    title: str
    need_chatgpt: bool = False


class CategoryUpdate(BaseModel):
    title: str | None
    need_chatgpt: bool | None


class Category(CategoryIn):
    id: int
    created: datetime
    user_id: int | None
    need_chatgpt: bool
