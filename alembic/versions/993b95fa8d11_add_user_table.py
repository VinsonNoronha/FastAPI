"""add user table 

Revision ID: 993b95fa8d11
Revises: d40cf8734c1e
Create Date: 2021-11-14 08:52:58.805526

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '993b95fa8d11'
down_revision = 'd40cf8734c1e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass
