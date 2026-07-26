"""
FollowUpRule - the model behind the Admin Portal's Follow-up Rules screen
(Milestone 15). Unlike BusinessRule's automation rules, which fire
synchronously right after an inbound message is analyzed, a follow-up
rule fires when NOTHING happens for a while: a customer messages in and
the business goes quiet. That's a time-based trigger, which is why this
milestone needed a scheduler (see app/scheduler/) - the rest of the
pipeline only ever reacts to events.
"""
import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.db.base import Base


class FollowUpRule(Base):
    __tablename__ = "follow_up_rules"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # How many hours a conversation can sit with an unanswered inbound
    # message before this rule considers it due.
    idle_hours: Mapped[int] = mapped_column(Integer, nullable=False)

    # Optional: only apply to contacts currently in this lead_status
    # (e.g. only chase "new" leads, not ones already "nurturing"). None
    # means any status - except won/lost, which are never chased.
    lead_status_filter: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)

    # The outbound message sent when the rule fires. Supports a
    # {display_name} placeholder, filled in per-contact at send time.
    message_template: Mapped[str] = mapped_column(Text, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
