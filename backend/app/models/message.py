"""
Message model - a single message within a Conversation, plus the
per-message AI annotations (sentiment, embedding reference) used for
retrieval and analytics.
"""
import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import ARRAY, DateTime, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base import Base
from app.models.conversation import Conversation  # noqa: F401  (needed for the relationship() type hint)


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=False)
    conversation: Mapped["Conversation"] = relationship()

    direction: Mapped[str] = mapped_column(String(8), nullable=False)  # "inbound" or "outbound"
    sender_type: Mapped[str] = mapped_column(String(16), nullable=False)  # "contact", "agent", "ai"
    body: Mapped[str] = mapped_column(Text, nullable=False)

    sentiment: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)

    # Gemini Embedding 2 vector for this message's body, used for semantic
    # search / similar-conversation retrieval (RAG). Stored as a plain float
    # array and searched with brute-force cosine similarity in Python - fine
    # at demo scale. At real scale, swap the Postgres column for pgvector and
    # do the similarity search as an indexed ANN query instead - the
    # retrieval service (app/ai/retrieval/) is the only place that would change.
    embedding: Mapped[Optional[list[float]]] = mapped_column(ARRAY(Float), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
