"""add ai_settings and prompt_templates tables

Revision ID: 0007
Revises: 0006
Create Date: 2026-07-23
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0007"
down_revision: Union[str, None] = "0006"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "ai_settings",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("chat_model", sa.String(100), server_default="gemini-3.5-flash", nullable=False),
        sa.Column("temperature", sa.Float(), server_default="0.7", nullable=False),
        sa.Column("auto_analysis_enabled", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("rag_enabled", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "prompt_templates",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("key", sa.String(64), nullable=False),
        sa.Column("custom_text", sa.Text(), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_prompt_templates_key", "prompt_templates", ["key"], unique=True)


def downgrade() -> None:
    op.drop_table("prompt_templates")
    op.drop_table("ai_settings")
