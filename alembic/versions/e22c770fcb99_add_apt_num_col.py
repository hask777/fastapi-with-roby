"""add apt num col

Revision ID: e22c770fcb99
Revises: 1fe43bc6891e
Create Date: 2023-06-01 17:29:54.150876

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e22c770fcb99'
down_revision = '1fe43bc6891e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('address',sa.Column('apt_num', sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column('address', 'apt_num')
