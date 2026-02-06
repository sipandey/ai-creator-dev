"""optimize indexes

Revision ID: 009_optimize_indexes
Revises: 008_add_strategies_table
Create Date: 2025-02-18 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '009_optimize_indexes'
down_revision: Union[str, None] = '008_add_strategies_table'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add index to scripts.user_id
    op.create_index(op.f('ix_scripts_user_id'), 'scripts', ['user_id'], unique=False)

    # Add unique index to creator_persona.user_id
    op.create_index(op.f('ix_creator_persona_user_id'), 'creator_persona', ['user_id'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_creator_persona_user_id'), table_name='creator_persona')
    op.drop_index(op.f('ix_scripts_user_id'), table_name='scripts')
