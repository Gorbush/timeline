"""empty message

Revision ID: b0ffd37de12c
Revises: 09bff0b9175e
Create Date: 2022-03-14 08:22:10.745662

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b0ffd37de12c'
down_revision = '09bff0b9175e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_faces_confidence_level'), 'faces', ['confidence_level'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_faces_confidence_level'), table_name='faces')
    # ### end Alembic commands ###
