"""add password hash field to guests table

Revision ID: 25ac22c48480
Revises: ee1c9c050f3f
Create Date: 2026-08-14 17:36:51.435240

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '25ac22c48480'
down_revision: Union[str, Sequence[str], None] = 'ee1c9c050f3f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.execute("""
        ALTER TABLE guests
        ADD COLUMN password_hash TEXT NOT NULL
    """)


def downgrade() -> None:
    """Downgrade schema."""

    op.execute("""
        ALTER TABLE guests
        DROP COLUMN password_hash
    """)
