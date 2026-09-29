"""update_guests_table

Revision ID: a17cf96588a7
Revises: 7f71e1615e40
Create Date: 2026-08-13 18:28:27.399419

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'a17cf96588a7'
down_revision: Union[str, Sequence[str], None] = '7f71e1615e40'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""--sql
        ALTER TABLE guests
        ADD role VARCHAR(20) NOT NULL DEFAULT 'user'
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""--sql
        ALTER TABLE guests
        DROP COLUMN role
    """)
