"""
PromptTemplate - an admin override for one of the AI pipeline's system
prompts, keyed by a fixed identifier ("conversation_analysis",
"suggested_reply"). custom_text is nullable: when empty/absent, the
pipeline falls back to the code-defined default in app/ai/prompts/ - see
app/services/prompt_settings_service.py, which is the only place that
resolves "what prompt actually runs right now".
"""
import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.db.base import Base


class PromptTemplate(Base):
    __tablename__ = "prompt_templates"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    key: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    custom_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
