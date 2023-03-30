"""add_system_category

Revision ID: 9ce7b339583f
Revises: 9a1febfe853a
Create Date: 2023-03-30 20:27:53.012200

"""
from alembic import op
import sqlalchemy as sa

from config import get_settings


settings = get_settings()


# revision identifiers, used by Alembic.
revision = "9ce7b339583f"
down_revision = "9a1febfe853a"
branch_labels = None
depends_on = None


def upgrade():
    for category in settings.system_categories:
        query = f"insert into category (title ) values ('{category}');"
        op.execute(query)


def downgrade():
    for category in settings.system_categories:
        query = f"delete from category where title = '{category}';"
        op.execute(query)
