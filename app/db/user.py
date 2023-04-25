from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    func,
)

from .base import metadata

user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(63), unique=True),
    Column("email", String(63), nullable=False, unique=True),
    Column("password", String(63)),
    Column("first_name", String(63)),
    Column("last_name", String(63)),
    Column("verified", Boolean, server_default="f", nullable=False),
    Column("subscriber", Boolean, server_default="f", nullable=False),
    Column("subscribe_end", DateTime),
    Column("created", DateTime, server_default=func.now()),
    Column("updated", DateTime),
)


token = Table(
    "token",
    metadata,
    Column(
        "user_id", Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    ),
    Column("value", String(63), unique=True, nullable=False),
)
