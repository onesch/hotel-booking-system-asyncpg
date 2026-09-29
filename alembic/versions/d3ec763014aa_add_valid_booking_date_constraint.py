"""add valid booking date constraint

Revision ID: d3ec763014aa
Revises: eaf080395245
Create Date: 2026-08-19 20:06:10.222598

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd3ec763014aa'
down_revision: Union[str, Sequence[str], None] = 'eaf080395245'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""--sql
        ALTER TABLE bookings
        ADD CONSTRAINT valid_booking_dates CHECK (check_out_date > check_in_date)
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""--sql
        ALTER TABLE bookings
        DROP CONSTRAINT valid_booking_dates
    """)
