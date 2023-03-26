from sqlalchemy import (
    Column,
    String,
    Table,
    ForeignKey,
    Text,
    Integer,
    DateTime,
    func,
)

from .base import metadata


category = Table(
    "category",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(31), nullable=False),
    Column("user_id", ForeignKey("user.id", ondelete="CASCADE"), nullable=False),
    Column("created", DateTime, server_default=func.now(), nullable=False),
)


card = Table(
    "card",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(255), nullable=False),
    Column("description", Text, nullable=False),
    Column("category_id", ForeignKey("category.id", ondelete="CASCADE")),
    Column("user_id", ForeignKey("user.id", ondelete="CASCADE"), nullable=False),
    Column("created", DateTime, server_default=func.now(), nullable=False),
    Column("updated", DateTime),
)

card_attachment = Table(
    "card_attachment",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("file", String(127), nullable=False),
    Column("created", DateTime, server_default=func.now(), nullable=False),
)
