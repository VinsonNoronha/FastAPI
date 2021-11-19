"""add phone number 

Revision ID: 13adef4dbe66
Revises: 8c8a04c9dbce
Create Date: 2021-11-14 08:50:08.966131

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '13adef4dbe66'
down_revision = '8c8a04c9dbce'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column(
        'phone_number', sa.String(), nullable=True))
    pass


def downgrade():
    op.drop_column('users', 'phone_number')
    pass
