"""Pydantic schemas for Message."""
import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class MessageRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    conversation_id: uuid.UUID
    direction: str
    sender_type: str
    body: str
    sentiment: Optional[str] = None
    created_at: datetime


class OutboundMessageCreate(BaseModel):
    """Body for an agent replying inside an existing conversation."""

    body: str = Field(min_length=1, max_length=4096)


class InboundMessageCreate(BaseModel):
    """
    Body for the /simulate/inbound endpoint - stands in for a real WhatsApp
    webhook payload. Lets us demo and test the full pipeline (contact
    creation -> conversation -> message) without real WhatsApp credentials.
    """

    phone_number: str = Field(min_length=5, max_length=32)
    display_name: Optional[str] = None
    body: str = Field(min_length=1, max_length=4096)


class SuggestedReplyResponse(BaseModel):
    suggested_reply: str
    used_similar_conversations: int = 0
