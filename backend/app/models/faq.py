"""
FAQ - a structured question/answer pair, kept as its own entity rather
than folded into the generic knowledge base. Unlike a document chunk (an
arbitrary slice of longer text), an FAQ is a deliberate, complete unit:
one specific question the business has chosen to answer a specific way -
worth its own admin screen and its own retrieval unit, embedded from
question+answer together so semantic search matches however a customer
actually phrases the question.
"""
import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import ARRAY, Boolean, DateTime, Float, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.db.base import Base


class FAQ(Base):
    __tablename__ = "faqs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    embedding: Mapped[Optional[list[float]]] = mapped_column(ARRAY(Float), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
