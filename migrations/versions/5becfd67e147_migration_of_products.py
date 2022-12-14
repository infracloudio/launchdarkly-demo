"""migration of products

Revision ID: 5becfd67e147
Revises: 2430c1c7268b
Create Date: 2022-09-26 11:21:12.745193

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5becfd67e147'
down_revision = '2430c1c7268b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('name', sa.String(length=200), nullable=True))
    op.add_column('products', sa.Column('description', sa.String(length=150), nullable=True))
    op.add_column('products', sa.Column('price', sa.Float(), nullable=True))
    op.add_column('products', sa.Column('image_url', sa.String(length=1000), nullable=True))
    op.add_column('products', sa.Column('product_type', sa.String(length=100), nullable=True))
    op.create_index(op.f('ix_products_description'), 'products', ['description'], unique=False)
    op.create_index(op.f('ix_products_name'), 'products', ['name'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_products_name'), table_name='products')
    op.drop_index(op.f('ix_products_description'), table_name='products')
    op.drop_column('products', 'product_type')
    op.drop_column('products', 'image_url')
    op.drop_column('products', 'price')
    op.drop_column('products', 'description')
    op.drop_column('products', 'name')
    # ### end Alembic commands ###
