"""Initial Version

Revision ID: d58a53f6c1d3
Revises: 
Create Date: 2022-03-10 14:23:30.578601

"""
from alembic import op
import sqlalchemy as sa
import timeline


# revision identifiers, used by Alembic.
revision = 'd58a53f6c1d3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('albums',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('smart', sa.Boolean(), nullable=True),
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.Column('rating', sa.Integer(), nullable=True),
    sa.Column('person_id', sa.Integer(), nullable=True),
    sa.Column('country', sa.String(length=100), nullable=True),
    sa.Column('state', sa.String(length=100), nullable=True),
    sa.Column('county', sa.String(length=100), nullable=True),
    sa.Column('village', sa.String(length=100), nullable=True),
    sa.Column('municipality', sa.String(length=100), nullable=True),
    sa.Column('camera_make', sa.String(length=100), nullable=True),
    sa.Column('thing_id', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('date_range',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('start_date')
    )
    op.create_table('gps',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('latitude', sa.Float(), nullable=True),
    sa.Column('longitude', sa.Float(), nullable=True),
    sa.Column('city', sa.String(length=100), nullable=True),
    sa.Column('road', sa.String(length=100), nullable=True),
    sa.Column('country_code', sa.String(length=10), nullable=True),
    sa.Column('country', sa.String(length=100), nullable=True),
    sa.Column('state', sa.String(length=100), nullable=True),
    sa.Column('postcode', sa.String(length=20), nullable=True),
    sa.Column('county', sa.String(length=100), nullable=True),
    sa.Column('village', sa.String(length=100), nullable=True),
    sa.Column('municipality', sa.String(length=100), nullable=True),
    sa.Column('display_address', sa.String(length=1000), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('persons',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=True),
    sa.Column('confirmed', sa.Boolean(), nullable=True),
    sa.Column('ignore', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_persons_ignore'), 'persons', ['ignore'], unique=False)
    op.create_table('section',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('dirty', sa.Boolean(), nullable=True),
    sa.Column('oldest_date', sa.DateTime(), nullable=True),
    sa.Column('newest_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('newest_date'),
    sa.UniqueConstraint('oldest_date')
    )
    op.create_table('things',
    sa.Column('id', sa.String(length=50), nullable=False),
    sa.Column('label_en', sa.String(length=100), nullable=True),
    sa.Column('parent_id', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['parent_id'], ['things.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('assets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('path', sa.String(length=512), nullable=True),
    sa.Column('filename', sa.String(length=100), nullable=True),
    sa.Column('directory', sa.String(length=512), nullable=True),
    sa.Column('ignore', sa.Boolean(), nullable=True),
    sa.Column('added', sa.DateTime(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('width', sa.Integer(), nullable=True),
    sa.Column('height', sa.Integer(), nullable=True),
    sa.Column('stars', sa.Integer(), nullable=True),
    sa.Column('score_aesthetic', sa.Float(), nullable=True),
    sa.Column('score_technical', sa.Float(), nullable=True),
    sa.Column('video_preview_generated', sa.Boolean(), nullable=True),
    sa.Column('video_fullscreen_transcoding_status', sa.Enum('NONE', 'WAITING', 'STARTED', 'DONE', name='transcodingstatus'), nullable=True),
    sa.Column('video_fullscreen_generated_progress', sa.Integer(), nullable=True),
    sa.Column('gps_id', sa.Integer(), nullable=True),
    sa.Column('section_id', sa.Integer(), nullable=True),
    sa.Column('no_creation_date', sa.Boolean(), nullable=True),
    sa.Column('asset_type', sa.Enum('jpg_photo', 'heic_photo', 'mov_video', 'mp4_video', 'avi_video', name='assettype'), nullable=True),
    sa.ForeignKeyConstraint(['gps_id'], ['gps.id'], ),
    sa.ForeignKeyConstraint(['section_id'], ['section.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('path')
    )
    op.create_index(op.f('ix_assets_added'), 'assets', ['added'], unique=False)
    op.create_index(op.f('ix_assets_created'), 'assets', ['created'], unique=False)
    op.create_index(op.f('ix_assets_ignore'), 'assets', ['ignore'], unique=False)
    op.create_table('status',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sections_dirty', sa.Boolean(), nullable=True),
    sa.Column('new_faces', sa.Boolean(), nullable=True),
    sa.Column('next_import_is_new', sa.Boolean(), nullable=True),
    sa.Column('last_import_album_id', sa.Integer(), nullable=True),
    sa.Column('in_sectioning', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['last_import_album_id'], ['albums.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('asset_album',
    sa.Column('asset_id', sa.Integer(), nullable=False),
    sa.Column('album_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['album_id'], ['albums.id'], ),
    sa.ForeignKeyConstraint(['asset_id'], ['assets.id'], ),
    sa.PrimaryKeyConstraint('asset_id', 'album_id')
    )
    op.create_table('asset_thing',
    sa.Column('asset_id', sa.Integer(), nullable=False),
    sa.Column('thing_id', sa.String(length=50), nullable=False),
    sa.ForeignKeyConstraint(['asset_id'], ['assets.id'], ),
    sa.ForeignKeyConstraint(['thing_id'], ['things.id'], ),
    sa.PrimaryKeyConstraint('asset_id', 'thing_id')
    )
    op.create_table('exif',
    sa.Column('key', sa.String(length=100), nullable=False),
    sa.Column('value', sa.String(length=100), nullable=True),
    sa.Column('asset_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['asset_id'], ['assets.id'], ),
    sa.PrimaryKeyConstraint('key', 'asset_id')
    )
    op.create_table('faces',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('person_id', sa.Integer(), nullable=True),
    sa.Column('asset_id', sa.Integer(), nullable=True),
    sa.Column('encoding', timeline.domain.NumpyType(), nullable=True),
    sa.Column('confidence_level', sa.Integer(), nullable=True),
    sa.Column('already_clustered', sa.Boolean(), nullable=True),
    sa.Column('distance_to_human_classified', sa.Integer(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('ignore', sa.Boolean(), nullable=True),
    sa.Column('x', sa.Integer(), nullable=True),
    sa.Column('y', sa.Integer(), nullable=True),
    sa.Column('w', sa.Integer(), nullable=True),
    sa.Column('h', sa.Integer(), nullable=True),
    sa.Column('confidence', sa.Float(), nullable=True),
    sa.Column('emotion', sa.String(length=20), nullable=True),
    sa.Column('emotion_confidence', sa.Float(), nullable=True),
    sa.Column('predicted_age', sa.Integer(), nullable=True),
    sa.Column('predicted_gender', sa.String(length=10), nullable=True),
    sa.ForeignKeyConstraint(['asset_id'], ['assets.id'], ),
    sa.ForeignKeyConstraint(['person_id'], ['persons.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_faces_distance_to_human_classified'), 'faces', ['distance_to_human_classified'], unique=False)
    op.create_index(op.f('ix_faces_ignore'), 'faces', ['ignore'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_faces_ignore'), table_name='faces')
    op.drop_index(op.f('ix_faces_distance_to_human_classified'), table_name='faces')
    op.drop_table('faces')
    op.drop_table('exif')
    op.drop_table('asset_thing')
    op.drop_table('asset_album')
    op.drop_table('status')
    op.drop_index(op.f('ix_assets_ignore'), table_name='assets')
    op.drop_index(op.f('ix_assets_created'), table_name='assets')
    op.drop_index(op.f('ix_assets_added'), table_name='assets')
    op.drop_table('assets')
    op.drop_table('things')
    op.drop_table('section')
    op.drop_index(op.f('ix_persons_ignore'), table_name='persons')
    op.drop_table('persons')
    op.drop_table('gps')
    op.drop_table('date_range')
    op.drop_table('albums')
    # ### end Alembic commands ###
