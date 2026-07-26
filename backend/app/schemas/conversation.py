"""Pydantic schemas for Conversation."""
import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.schemas.contact import ContactRead
from app.schemas.message import MessageRead


class ConversationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    status: str
    intent: Optional[str] = None
    ai_summary: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class ConversationListItem(ConversationRead):
    """Conversation shape used in the inbox list - includes the contact and
    a preview of the most recent message so the sidebar can render without
    a second round-trip per conversation."""

    contact: ContactRead
    last_message: Optional[MessageRead] = None


class ConversationDetail(ConversationRead):
    """Conversation shape used when a thread is opened - includes the full
    message history."""

    contact: ContactRead
    messages: list[MessageRead] = []
