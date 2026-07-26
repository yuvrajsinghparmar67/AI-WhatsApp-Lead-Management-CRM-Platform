"""add embedding column to messages

Revision ID: 0002
Revises: 0001
Create Date: 2026-07-22
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "messages",
        sa.Column("embedding", postgresql.ARRAY(sa.Float()), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("messages", "embedding")
