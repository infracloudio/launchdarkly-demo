"""migration of products

Revision ID: 9695a2f5b8ee
Revises: 5becfd67e147
Create Date: 2022-09-26 11:36:59.065608

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9695a2f5b8ee'
down_revision = '5becfd67e147'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('on_sale', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('products', 'on_sale')
    # ### end Alembic commands ###
