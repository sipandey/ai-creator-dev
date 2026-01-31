"""change creator_type to string

Revision ID: 3bfbdae4493e
Revises: 1eb399115807
Create Date: 2026-01-14 01:44:57.039777

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3bfbdae4493e'
down_revision: Union[str, Sequence[str], None] = '1eb399115807'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column(
        "users",
        "creator_type",
        type_=sa.String(),
        existing_nullable=False,
    )

def downgrade():
    pass

