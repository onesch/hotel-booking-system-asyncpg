"""update_room_type_field

Revision ID: 7f71e1615e40
Revises: 
Create Date: 2026-08-12 17:24:38.421646

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7f71e1615e40'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint(
        constraint_name="room_types_room_type_check",
        table_name="room_types",
        type_="check",
    )

    op.create_unique_constraint(
        constraint_name="room_types_room_type_key",
        table_name="room_types",
        columns=["room_type"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        constraint_name="room_types_room_type_key",
        table_name="room_types",
        type_="unique",
    )

    op.execute("""
        DELETE FROM room_types
        WHERE room_type NOT IN ('Single', 'Double', 'Deluxe')
    """)

    op.create_check_constraint(
        constraint_name="room_types_room_type_check",
        table_name="room_types",
        condition="room_type IN ('Single', 'Double', 'Deluxe')",
    )
