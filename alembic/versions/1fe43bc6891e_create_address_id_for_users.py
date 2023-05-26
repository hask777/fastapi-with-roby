"""create address_id for users

Revision ID: 1fe43bc6891e
Revises: 77970ff56eb3
Create Date: 2023-05-22 11:28:32.635871

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1fe43bc6891e'
down_revision = '77970ff56eb3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('address_id', sa.Integer(), nullable=True))
    op.create_foreign_key('address_users_fk', source_table='users', referent_table='address',
                           local_cols=['address_id'], remote_cols=['id'], ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint('address_users_fk', table_name='users')
    op.drop_column('users', 'address_id')
