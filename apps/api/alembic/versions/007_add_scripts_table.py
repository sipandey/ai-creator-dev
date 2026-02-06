"""add scripts table

Revision ID: 007_add_scripts_table
Revises: 006_enhance_persona_system
Create Date: 2024-05-23 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '007_add_scripts_table'
down_revision: Union[str, None] = '006_enhance_persona_system'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('scripts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('topic', sa.String(), nullable=False),
    sa.Column('script_json', sa.JSON(), nullable=False),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('performance_data', sa.JSON(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_scripts_id'), 'scripts', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_scripts_id'), table_name='scripts')
    op.drop_table('scripts')
