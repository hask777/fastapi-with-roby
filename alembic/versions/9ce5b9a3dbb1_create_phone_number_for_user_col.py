"""create phone number for user col

Revision ID: 9ce5b9a3dbb1
Revises: 
Create Date: 2023-05-22 10:06:43.045175

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9ce5b9a3dbb1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'phone_number')
