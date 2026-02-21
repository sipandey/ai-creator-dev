"""add index to scripts user_id

Revision ID: 28f5850cb767
Revises: 008_add_strategies_table
Create Date: 2026-02-21 20:41:18.710440

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '28f5850cb767'
down_revision: Union[str, Sequence[str], None] = '008_add_strategies_table'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_index(op.f('ix_scripts_user_id'), 'scripts', ['user_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_scripts_user_id'), table_name='scripts')
