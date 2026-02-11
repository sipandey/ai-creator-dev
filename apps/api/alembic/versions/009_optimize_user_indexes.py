"""optimize user indexes

Revision ID: 009_optimize_user_indexes
Revises: 008_add_strategies_table
Create Date: 2024-05-23 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '009_optimize_user_indexes'
down_revision: Union[str, None] = '008_add_strategies_table'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index(op.f('ix_scripts_user_id'), 'scripts', ['user_id'], unique=False)
    op.create_index(op.f('ix_content_strategies_user_id'), 'content_strategies', ['user_id'], unique=False)
    op.create_index(op.f('ix_creator_persona_user_id'), 'creator_persona', ['user_id'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_creator_persona_user_id'), table_name='creator_persona')
    op.drop_index(op.f('ix_content_strategies_user_id'), table_name='content_strategies')
    op.drop_index(op.f('ix_scripts_user_id'), table_name='scripts')
