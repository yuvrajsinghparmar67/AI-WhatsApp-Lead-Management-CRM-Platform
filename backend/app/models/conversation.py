"""
Conversation model - one active thread between the business and a Contact.
Holds AI-generated conversation-level metadata (summary, intent) that gets
refreshed as new messages arrive, rather than recomputed from scratch on
every read.
"""
import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base import Base
from app.models.contact import Contact  # noqa: F401  (needed for the relationship() type hint)


class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    contact_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("contacts.id"), nullable=False)

    contact: Mapped["Contact"] = relationship(back_populates="conversations")

    status: Mapped[str] = mapped_column(String(16), default="open")  # open, snoozed, closed
    intent: Mapped[str] = mapped_column(String(64), nullable=True)  # AI-detected intent label
    ai_summary: Mapped[str] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
