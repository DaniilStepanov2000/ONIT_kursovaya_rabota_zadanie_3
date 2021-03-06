"""empty message

Revision ID: 836d3e82b3da
Revises: 48724c37c2f8
Create Date: 2022-03-27 20:13:46.445844

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '836d3e82b3da'
down_revision = '48724c37c2f8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('doctors', sa.Column('hospital_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'doctors', 'hospitals', ['hospital_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'doctors', type_='foreignkey')
    op.drop_column('doctors', 'hospital_id')
    # ### end Alembic commands ###
