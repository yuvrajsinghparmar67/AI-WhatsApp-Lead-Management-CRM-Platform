"""
Contact model - represents a customer/lead who messages the business.
This is the core CRM entity that AI-derived fields (lead score, sentiment,
priority, etc.) attach to.
"""
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Contact(Base):
    __tablename__ = "contacts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phone_number: Mapped[str] = mapped_column(String(32), unique=True, index=True, nullable=False)
    display_name: Mapped[str] = mapped_column(String(255), nullable=True)

    # AI-derived CRM fields (populated by the AI pipeline as conversations happen)
    lead_status: Mapped[str] = mapped_column(String(32), default="new")  # new, qualified, nurturing, won, lost
    priority: Mapped[str] = mapped_column(String(16), default="medium")  # low, medium, high, urgent
    sentiment: Mapped[str] = mapped_column(String(16), nullable=True)  # positive, neutral, negative
    estimated_budget: Mapped[float] = mapped_column(Float, nullable=True)
    confidence_score: Mapped[float] = mapped_column(Float, nullable=True)  # 0-1, AI's confidence in its own read

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    conversations: Mapped[list["Conversation"]] = relationship(back_populates="contact")
