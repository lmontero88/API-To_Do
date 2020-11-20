"""empty message

Revision ID: d10d7b0e2d13
Revises: 4a5b3725bc3b
Create Date: 2020-11-19 23:25:18.055818

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd10d7b0e2d13'
down_revision = '4a5b3725bc3b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('user', table_name='list')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('user', 'list', ['user'], unique=True)
    # ### end Alembic commands ###