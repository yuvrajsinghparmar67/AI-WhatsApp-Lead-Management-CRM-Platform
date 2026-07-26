"""Pydantic schemas for the semantic-search / RAG endpoints."""
import uuid
from typing import Optional

from pydantic import BaseModel


class SimilarConversationItem(BaseModel):
    conversation_id: uuid.UUID
    contact_name: str
    snippet: str
    similarity: float
    ai_summary: Optional[str] = None
