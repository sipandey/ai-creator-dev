"""Enhance persona system with video processing support

Revision ID: 006_enhance_persona_system
Revises: f983991d4401
Create Date: 2024-01-15 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '006_enhance_persona_system'
down_revision = 'f983991d4401'
branch_labels = None
depends_on = None

def upgrade():
    # Add new columns to existing creator_persona table (non-breaking)
    op.add_column('creator_persona', sa.Column('version', sa.String(10), server_default='v1'))
    op.add_column('creator_persona', sa.Column('content_sources', sa.JSON(), nullable=True))
    op.add_column('creator_persona', sa.Column('processing_metadata', sa.JSON(), nullable=True))
    
    # Create content_sources table for tracking input sources
    op.create_table('content_sources',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('creator_id', sa.Integer(), nullable=False),
        sa.Column('source_url', sa.String(500), nullable=True),
        sa.Column('source_type', sa.String(50), nullable=False),  # 'video', 'text', 'manual'
        sa.Column('platform', sa.String(50), nullable=True),  # 'instagram', 'youtube', 'tiktok'
        sa.Column('content_data', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('confidence_contribution', sa.Float(), server_default='0.0'),
        sa.Column('processed_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('is_active', sa.Boolean(), server_default='true'),
        sa.ForeignKeyConstraint(['creator_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_content_sources_id'), 'content_sources', ['id'], unique=False)
    op.create_index(op.f('ix_content_sources_creator_id'), 'content_sources', ['creator_id'], unique=False)
    op.create_index(op.f('ix_content_sources_source_type'), 'content_sources', ['source_type'], unique=False)
    
    # Create persona_versions table for tracking persona evolution
    op.create_table('persona_versions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('creator_id', sa.Integer(), nullable=False),
        sa.Column('version_number', sa.Integer(), nullable=False),
        sa.Column('persona_data', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('confidence_score', sa.Float(), nullable=True),
        sa.Column('change_summary', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['creator_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('creator_id', 'version_number', name='uq_creator_version')
    )
    op.create_index(op.f('ix_persona_versions_id'), 'persona_versions', ['id'], unique=False)
    op.create_index(op.f('ix_persona_versions_creator_id'), 'persona_versions', ['creator_id'], unique=False)

def downgrade():
    # Drop new tables
    op.drop_index(op.f('ix_persona_versions_creator_id'), table_name='persona_versions')
    op.drop_index(op.f('ix_persona_versions_id'), table_name='persona_versions')
    op.drop_table('persona_versions')
    
    op.drop_index(op.f('ix_content_sources_source_type'), table_name='content_sources')
    op.drop_index(op.f('ix_content_sources_creator_id'), table_name='content_sources')
    op.drop_index(op.f('ix_content_sources_id'), table_name='content_sources')
    op.drop_table('content_sources')
    
    # Remove new columns from creator_persona
    op.drop_column('creator_persona', 'processing_metadata')
    op.drop_column('creator_persona', 'content_sources')
    op.drop_column('creator_persona', 'version')