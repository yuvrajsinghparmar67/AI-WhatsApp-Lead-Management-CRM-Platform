"""
BusinessRule - the pipeline stage between Knowledge Retrieval and Gemini
that didn't exist before this milestone. Two kinds, one table:

- "guardrail": a free-text constraint (e.g. "Never discuss refunds without
  human approval") injected into every suggested-reply prompt as a
  MANDATORY instruction - this directly implements the diagram's
  Knowledge Retrieval -> Business Rules -> Gemini ordering.
- "automation": a structured condition -> action rule (e.g. "if sentiment
  = negative, set priority = urgent") applied deterministically after the
  AI's own analysis runs, so an admin's explicit policy can override or
  extend what the model inferred - the same idea as Salesforce workflow
  rules, applied to the CRM Update stage.
"""
import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.db.base import Base


class BusinessRule(Base):
    __tablename__ = "business_rules"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    rule_type: Mapped[str] = mapped_column(String(16), nullable=False)  # "guardrail" or "automation"
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # --- guardrail fields ---
    guardrail_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # --- automation fields: "if <trigger_field> is <trigger_value>, set <action_field> to <action_value>" ---
    trigger_field: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)   # "intent", "sentiment", "priority"
    trigger_value: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    action_field: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)    # "lead_status", "priority"
    action_value: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
