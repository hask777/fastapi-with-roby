"""Create address table

Revision ID: 77970ff56eb3
Revises: 9ce5b9a3dbb1
Create Date: 2023-05-22 11:09:04.874323

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '77970ff56eb3'
down_revision = '9ce5b9a3dbb1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('address',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('address1', sa.String(), nullable=False),
        sa.Column('address2', sa.String(), nullable=False),
        sa.Column('city', sa.String(), nullable=False),
        sa.Column('state', sa.String(), nullable=False),
        sa.Column('country', sa.String(), nullable=False),
        sa.Column('postalcode', sa.String(), nullable=False),
    )

def downgrade() -> None:
    op.drop_table('address')
