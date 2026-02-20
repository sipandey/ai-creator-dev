"""add script user_id index

Revision ID: 009_add_script_user_id_index
Revises: 008_add_strategies_table
Create Date: 2024-05-24 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '009_add_script_user_id_index'
down_revision: Union[str, None] = '008_add_strategies_table'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index(op.f('ix_scripts_user_id'), 'scripts', ['user_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_scripts_user_id'), table_name='scripts')
