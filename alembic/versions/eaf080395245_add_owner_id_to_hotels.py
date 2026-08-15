"""add owner_id to hotels

Revision ID: eaf080395245
Revises: 25ac22c48480
Create Date: 2026-08-15 20:41:42.579046

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eaf080395245'
down_revision: Union[str, Sequence[str], None] = '25ac22c48480'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""--sql
        ALTER TABLE hotels
        ADD COLUMN owner_id INTEGER NOT NULL
    """)

    op.execute("""--sql
        ALTER TABLE hotels
        ADD CONSTRAINT fk_hotels_owner_id_guests
        FOREIGN KEY (owner_id)
        REFERENCES guests(id)
        ON DELETE CASCADE
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""--sql
        ALTER TABLE hotels
        DROP CONSTRAINT fk_hotels_owner_id_guests
    """)

    op.execute("""--sql
        ALTER TABLE hotels
        DROP COLUMN owner_id
    """)
