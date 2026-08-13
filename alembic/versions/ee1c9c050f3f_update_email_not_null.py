"""update_email_not_null

Revision ID: ee1c9c050f3f
Revises: a17cf96588a7
Create Date: 2026-08-13 18:46:30.648491

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ee1c9c050f3f'
down_revision: Union[str, Sequence[str], None] = 'a17cf96588a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""--sql
        ALTER TABLE guests
        ALTER COLUMN email SET NOT NULL;
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""--sql
        ALTER TABLE guests
        ALTER COLUMN email SET NOT NULL;
    """)
