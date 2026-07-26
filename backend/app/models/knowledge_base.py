"""
Knowledge base models: a KnowledgeBaseDocument (a manual entry like a
pricing plan, or an uploaded PDF/DOCX/TXT) is split into one or more
KnowledgeBaseChunks, each independently embedded - the same
embed-and-search pattern already used for Messages (see app/ai/retrieval),
just applied to company facts instead of conversation history.

Chunking a document rather than embedding it whole keeps each embedded
unit small and topically focused, which is what makes semantic search
actually precise for longer uploaded documents.
"""
import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import ARRAY, DateTime, ForeignKey, Float, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base import Base


class KnowledgeBaseDocument(Base):
    __tablename__ = "knowledge_base_documents"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    source_type: Mapped[str] = mapped_column(String(16), nullable=False)  # "manual", "pdf", "docx", "txt"
    original_filename: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    chunks: Mapped[list["KnowledgeBaseChunk"]] = relationship(
        back_populates="document", cascade="all, delete-orphan", order_by="KnowledgeBaseChunk.chunk_index"
    )


class KnowledgeBaseChunk(Base):
    __tablename__ = "knowledge_base_chunks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("knowledge_base_documents.id", ondelete="CASCADE"), nullable=False
    )
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    embedding: Mapped[Optional[list[float]]] = mapped_column(ARRAY(Float), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    document: Mapped["KnowledgeBaseDocument"] = relationship(back_populates="chunks")
