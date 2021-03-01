"""add user password_hash column

Revision ID: 87524a43f720
Revises: d1d869f0483f
Create Date: 2021-02-28 00:19:56.626875

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '87524a43f720'
down_revision = 'd1d869f0483f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password_hash', sa.String(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'password_hash')
    # ### end Alembic commands ###
