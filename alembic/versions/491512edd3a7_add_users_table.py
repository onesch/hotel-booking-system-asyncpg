"""add_users_table

Revision ID: 491512edd3a7
Revises: 7f71e1615e40
Create Date: 2026-08-12 17:51:08.329130

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '491512edd3a7'
down_revision: Union[str, Sequence[str], None] = '7f71e1615e40'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
            email VARCHAR(255) NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role VARCHAR(20) NOT NULL DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            CONSTRAINT users_role_check
                CHECK (role IN ('user', 'admin'))
        );
    """)

    op.execute("""
        ALTER TABLE Guests
        DROP COLUMN IF EXISTS created_at,
        DROP COLUMN IF EXISTS email;
    """)

    op.execute("""
        ALTER TABLE Guests
        ADD COLUMN user_id INTEGER;

        ALTER TABLE Guests
        ADD CONSTRAINT fk_guest_user
            FOREIGN KEY (user_id)
            REFERENCES Users(id)
            ON DELETE CASCADE;
    """)


def downgrade() -> None:
    """Downgrade schema."""

    op.execute("""
        ALTER TABLE Guests
        DROP CONSTRAINT IF EXISTS fk_guest_user,
        DROP COLUMN IF EXISTS user_id;
    """)

    op.execute("""
        ALTER TABLE Guests
        ADD COLUMN email VARCHAR(255),
        ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
    """)

    op.execute("""
        DROP TABLE IF EXISTS Users;
    """)
