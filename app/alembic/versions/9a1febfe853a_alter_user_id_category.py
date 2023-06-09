"""alter_user_id_category

Revision ID: 9a1febfe853a
Revises: 7701114d9447
Create Date: 2023-03-30 20:25:06.315658

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "9a1febfe853a"
down_revision = "7701114d9447"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("category", "user_id", existing_type=sa.INTEGER(), nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("category", "user_id", existing_type=sa.INTEGER(), nullable=False)
    # ### end Alembic commands ###
