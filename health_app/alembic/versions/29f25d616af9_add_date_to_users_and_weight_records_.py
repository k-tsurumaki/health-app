"""add_date_to_users_and_weight_records_tables

Revision ID: 29f25d616af9
Revises: a09ecc26b6ff
Create Date: 2024-12-17 20:35:42.204955

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '29f25d616af9'
down_revision: Union[str, None] = 'a09ecc26b6ff'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('meals', sa.Column('date', sa.Date(), nullable=False))
    op.drop_column('meals', 'date_time')
    op.add_column('weight_records', sa.Column('date', sa.Date(), nullable=False))
    op.drop_column('weight_records', 'date_time')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('weight_records', sa.Column('date_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    op.drop_column('weight_records', 'date')
    op.add_column('meals', sa.Column('date_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    op.drop_column('meals', 'date')
    # ### end Alembic commands ###
