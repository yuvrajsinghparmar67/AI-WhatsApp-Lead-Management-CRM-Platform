"""add role column to users

Revision ID: 0008
Revises: 0007
Create Date: 2026-07-23

On a fresh database this is a no-op beyond adding the column (the first
registration through the API becomes admin - see auth.py::register). On
an EXISTING database from an earlier milestone, adding the column with
server_default="agent" would otherwise silently demote whoever was
already using the app - so this migration also promotes the single
earliest-created existing user (if any) to admin, preserving access
across the upgrade instead of locking everyone out.
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0008"
down_revision: Union[str, None] = "0007"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("role", sa.String(16), server_default="agent", nullable=False))

    connection = op.get_bind()
    connection.execute(
        sa.text(
            """
            UPDATE users SET role = 'admin'
            WHERE id = (SELECT id FROM users ORDER BY created_at ASC LIMIT 1)
            """
        )
    )


def downgrade() -> None:
    op.drop_column("users", "role")
