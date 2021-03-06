"""image path column to users model

Revision ID: ba177711fc7f
Revises: 052bd70f873f
Create Date: 2020-11-27 11:33:07.054662

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba177711fc7f'
down_revision = '052bd70f873f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('path_to_image', sa.String(length=50), nullable=True))
    op.create_unique_constraint(None, 'users', ['path_to_image'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'path_to_image')
    # ### end Alembic commands ###
