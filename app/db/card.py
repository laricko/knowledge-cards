from sqlalchemy import (
    Column,
    String,
    Table,
    ForeignKey,
    Text,
    Integer,
    DateTime,
    func,
    Boolean,
    UniqueConstraint,
)

from .base import metadata


category = Table(
    "category",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(31), nullable=False),
    Column("user_id", ForeignKey("user.id", ondelete="CASCADE")),
    Column("created", DateTime, server_default=func.now(), nullable=False),
    Column("need_chatgpt", Boolean, server_default="f"),
    UniqueConstraint("title", "user_id", name="title_user_unique_category"),
)


related_system_categories_with_user = Table(
    "related_system_categories_with_user",
    metadata,
    Column("category_id", ForeignKey("category.id", ondelete="CASCADE")),
    Column("user_id", ForeignKey("user.id", ondelete="CASCADE")),
    UniqueConstraint(
        "category_id",
        "user_id",
        name="category_user_unique_related_system_categories_with_user",
    ),
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
    Column("need_chatgpt", Boolean, server_default="f"),
    UniqueConstraint("title", "user_id", name="title_user_unique_card"),
)

card_attachment = Table(
    "card_attachment",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("file", String(127), nullable=False),
    Column("created", DateTime, server_default=func.now(), nullable=False),
)
