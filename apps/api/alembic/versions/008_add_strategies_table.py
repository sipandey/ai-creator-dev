"""add content strategies table

Revision ID: 008_add_strategies_table
Revises: 007_add_scripts_table
Create Date: 2024-05-23 11:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '008_add_strategies_table'
down_revision: Union[str, None] = '007_add_scripts_table'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('content_strategies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('week_start_date', sa.Date(), nullable=False),
    sa.Column('strategy_json', sa.JSON(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_content_strategies_id'), 'content_strategies', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_content_strategies_id'), table_name='content_strategies')
    op.drop_table('content_strategies')
