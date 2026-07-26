"""add follow_up_rules and follow_up_logs tables

Revision ID: 0009
Revises: 0008
Create Date: 2026-07-24
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0009"
down_revision: Union[str, None] = "0008"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "follow_up_rules",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("idle_hours", sa.Integer(), nullable=False),
        sa.Column("lead_status_filter", sa.String(32), nullable=True),
        sa.Column("message_template", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "follow_up_logs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("rule_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("follow_up_rules.id"), nullable=False),
        sa.Column("conversation_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("conversations.id"), nullable=False),
        sa.Column("contact_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("contacts.id"), nullable=False),
        sa.Column("message_body", sa.Text(), nullable=False),
        sa.Column("sent_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_follow_up_logs_rule_conversation", "follow_up_logs", ["rule_id", "conversation_id"])


def downgrade() -> None:
    op.drop_index("ix_follow_up_logs_rule_conversation", table_name="follow_up_logs")
    op.drop_table("follow_up_logs")
    op.drop_table("follow_up_rules")
