"""add indexes to scripts and strategies

Revision ID: a1b2c3d4e5f6
Revises: f983991d4401
Create Date: 2025-01-28 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = 'f983991d4401'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index(op.f('ix_scripts_user_id'), 'scripts', ['user_id'], unique=False)
    op.create_index(op.f('ix_content_strategies_user_id'), 'content_strategies', ['user_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_content_strategies_user_id'), table_name='content_strategies')
    op.drop_index(op.f('ix_scripts_user_id'), table_name='scripts')
