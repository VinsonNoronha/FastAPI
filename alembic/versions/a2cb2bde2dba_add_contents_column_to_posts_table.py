"""add contents column to posts table 

Revision ID: a2cb2bde2dba
Revises: ab7bacbcd8d9
Create Date: 2021-11-14 11:01:48.759042

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a2cb2bde2dba'
down_revision = 'ab7bacbcd8d9'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
