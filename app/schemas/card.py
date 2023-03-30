from enum import Enum
from datetime import datetime

from pydantic import BaseModel


class CardsOrdering(str, Enum):
    id = "id"
    d_id = "-id"
    title = "title"
    d_title = "-title"
    created = "created"
    d_created = "-created"
    updated = "updated"
    d_updated = "-updated"


class CardIn(BaseModel):
    title: str
    description: str
    category_id: int | None
    need_chatgpt: bool | None


class CardUpdate(BaseModel):
    title: str | None
    description: str | None
    category_id: int | None
    need_chatgpt: bool | None


class Card(CardIn):
    id: int
    created: datetime
    updated: datetime | None
