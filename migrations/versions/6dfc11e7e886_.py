"""empty message

Revision ID: 6dfc11e7e886
Revises: 
Create Date: 2017-01-28 10:41:09.709096

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6dfc11e7e886'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=128), nullable=True),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('body_html', sa.Text(), nullable=True),
    sa.Column('summary', sa.String(length=200), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('posts')
    # ### end Alembic commands ###