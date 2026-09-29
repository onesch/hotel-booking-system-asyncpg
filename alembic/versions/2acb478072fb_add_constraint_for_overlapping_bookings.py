"""add constraint for overlapping bookings

Revision ID: 2acb478072fb
Revises: d3ec763014aa
Create Date: 2026-08-19 20:28:44.214602

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2acb478072fb'
down_revision: Union[str, Sequence[str], None] = 'd3ec763014aa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""--sql
        CREATE EXTENSION IF NOT EXISTS btree_gist
    """)
    op.execute("""--sql
        ALTER TABLE bookings
        ADD CONSTRAINT no_overlapping_bookings
        EXCLUDE USING gist (
            room_id WITH =,
            daterange(check_in_date, check_out_date, '[)') WITH &&
        )
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""--sql
        ALTER TABLE bookings
        DROP CONSTRAINT IF EXISTS no_overlapping_bookings
    """)

    op.execute("""--sql
        DROP EXTENSION IF EXISTS btree_gist
    """)
