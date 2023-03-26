from sqlalchemy import (
    Column,
    Integer,
    String,
    Table,
    Boolean,
    ForeignKey,
    DateTime,
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
    Column("created", DateTime, server_default=func.now()),
    Column("updated", DateTime),
)

# function `update_datetime_updated_column`
# trigger `update_datetime_updated_column_trigger`
# look in `app/alembic/versions/c22ed0931890_add_created_and_updated_columns_to_user.py`


token = Table(
    "token",
    metadata,
    Column(
        "user_id", Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    ),
    Column("value", String(63), unique=True, nullable=False),
)
