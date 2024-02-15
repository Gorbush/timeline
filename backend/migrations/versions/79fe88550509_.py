"""empty message

Revision ID: 79fe88550509
Revises: dd6dce813ff5
Create Date: 2024-02-12 22:27:37.557830

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '79fe88550509'
down_revision = 'dd6dce813ff5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_assets_checksum'), 'assets', ['checksum'], unique=False)
    op.create_index(op.f('ix_assets_filename'), 'assets', ['filename'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_assets_filename'), table_name='assets')
    op.drop_index(op.f('ix_assets_checksum'), table_name='assets')
    # ### end Alembic commands ###
