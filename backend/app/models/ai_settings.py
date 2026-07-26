"""
AISettings - a SINGLETON row (same pattern as Company) controlling AI
pipeline behavior at runtime, without a redeploy.

Deliberately does NOT expose the embedding model as editable: swapping
embedding models would silently invalidate every existing stored
embedding (different models produce vectors of different dimensions/
meaning), breaking semantic search across the whole app until everything
was re-embedded. That's a real migration operation, not a settings
toggle - so it's left out rather than shipped as a trap.
"""
import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.db.base import Base


class AISettings(Base):
    __tablename__ = "ai_settings"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chat_model: Mapped[str] = mapped_column(String(100), default="gemini-3.5-flash")
    temperature: Mapped[float] = mapped_column(Float, default=0.7)
    auto_analysis_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    rag_enabled: Mapped[bool] = mapped_column(Boolean, default=True)

    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
