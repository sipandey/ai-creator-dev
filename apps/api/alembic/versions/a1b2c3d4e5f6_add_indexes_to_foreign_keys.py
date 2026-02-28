"""add_indexes_to_foreign_keys

Revision ID: a1b2c3d4e5f6
Revises: f983991d4401
Create Date: 2023-11-20 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1b2c3d4e5f6'
down_revision = 'f983991d4401'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add index to content_sources
    op.create_index('ix_content_sources_creator_id', 'content_sources', ['creator_id'], unique=False)

    # Add index to content_strategies
    op.create_index('ix_content_strategies_user_id', 'content_strategies', ['user_id'], unique=False)

    # Add index to creator_persona
    op.create_index('ix_creator_persona_user_id', 'creator_persona', ['user_id'], unique=False)

    # Add index to feedback
    op.create_index('ix_feedback_user_id', 'feedback', ['user_id'], unique=False)

    # Add index to preferences
    op.create_index('ix_preferences_user_id', 'preferences', ['user_id'], unique=False)

    # Add index to scripts
    op.create_index('ix_scripts_user_id', 'scripts', ['user_id'], unique=False)


def downgrade() -> None:
    # Remove index from content_sources
    op.drop_index('ix_content_sources_creator_id', table_name='content_sources')

    # Remove index from content_strategies
    op.drop_index('ix_content_strategies_user_id', table_name='content_strategies')

    # Remove index from creator_persona
    op.drop_index('ix_creator_persona_user_id', table_name='creator_persona')

    # Remove index from feedback
    op.drop_index('ix_feedback_user_id', table_name='feedback')

    # Remove index from preferences
    op.drop_index('ix_preferences_user_id', table_name='preferences')

    # Remove index from scripts
    op.drop_index('ix_scripts_user_id', table_name='scripts')
