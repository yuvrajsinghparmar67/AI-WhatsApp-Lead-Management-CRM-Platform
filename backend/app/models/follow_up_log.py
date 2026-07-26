"""
FollowUpLog - one row per follow-up message actually sent. Serves two
purposes: it's the admin-facing "recent activity" feed for the Follow-up
Rules screen, and it's how the scheduler avoids sending the same rule to
the same conversation twice for one quiet period (see
follow_up_rule_service.run_due_follow_ups).
"""
import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base import Base
from app.models.contact import Contact  # noqa: F401  (needed for the relationship() type hint)
from app.models.follow_up_rule import FollowUpRule  # noqa: F401  (needed for the relationship() type hint)


class FollowUpLog(Base):
    __tablename__ = "follow_up_logs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    rule_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("follow_up_rules.id"), nullable=False)
    conversation_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=False)
    contact_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("contacts.id"), nullable=False)

    # Snapshot of what was actually sent - kept even if the rule's template
    # is edited or deleted later, so the activity feed stays accurate.
    message_body: Mapped[str] = mapped_column(Text, nullable=False)

    sent_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    rule: Mapped["FollowUpRule"] = relationship()
    contact: Mapped["Contact"] = relationship()
