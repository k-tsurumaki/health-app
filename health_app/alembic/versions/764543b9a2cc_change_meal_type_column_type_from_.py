"""Change meal_type column type from String to Enum

Revision ID: 764543b9a2cc
Revises: 29f25d616af9
Create Date: 2024-12-31 08:35:41.328157

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from health_app.backend.schemas import MealType

# revision identifiers, used by Alembic.
revision: str = '764543b9a2cc'
down_revision: Union[str, None] = '29f25d616af9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Convert the external Enum class to a SQLAlchemy Enum type
meal_type_enum = sa.Enum(MealType, name='mealtype', create_type=True)


def upgrade() -> None:
    # Create the new Enum type in the database
    meal_type_enum.create(op.get_bind(), checkfirst=True)

    op.execute(
        """
        ALTER TABLE meals 
        ALTER COLUMN meal_type TYPE mealtype 
        USING meal_type::mealtype
        """
    )
    # Alter the column to use the new Enum type
    op.alter_column(
        'meals', 'meal_type',
        existing_type=sa.VARCHAR(length=50),
        type_=meal_type_enum,
        existing_nullable=False
    )
    


def downgrade() -> None:
    op.execute(
        """
        ALTER TABLE meals 
        ALTER COLUMN meal_type TYPE VARCHAR(50)
        """
    )
    # Revert the column to its previous type
    op.alter_column(
        'meals', 'meal_type',
        existing_type=meal_type_enum,
        type_=sa.VARCHAR(length=50),
        existing_nullable=False
    )
    

    # Drop the Enum type from the database
    meal_type_enum.drop(op.get_bind(), checkfirst=True)

