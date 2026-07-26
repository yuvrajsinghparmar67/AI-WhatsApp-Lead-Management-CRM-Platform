"""Pydantic schemas for the knowledge base."""
import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class KnowledgeBaseDocumentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    source_type: str
    original_filename: str | None = None
    chunk_count: int
    created_at: datetime


class ManualEntryCreate(BaseModel):
    """
    Body for adding a knowledge base entry by typing it in directly -
    e.g. a pricing plan like "Premium Gym Membership: ₹2500/month,
    unlimited access, personal trainer included" - rather than uploading a file.
    """

    title: str = Field(min_length=1, max_length=255)
    content: str = Field(min_length=1, max_length=20000)
