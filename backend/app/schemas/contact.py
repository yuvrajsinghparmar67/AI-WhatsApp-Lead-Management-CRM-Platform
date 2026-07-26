"""Pydantic schemas for Contact - the customer/lead entity."""
import uuid
from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict


class ContactRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    phone_number: str
    display_name: Optional[str] = None
    lead_status: str
    priority: str
    sentiment: Optional[str] = None
    estimated_budget: Optional[float] = None
    confidence_score: Optional[float] = None
    created_at: datetime
    updated_at: datetime


class ContactUpdate(BaseModel):
    """
    Manual override for AI-derived fields. Lets an agent move a card on the
    lead pipeline board (drag-and-drop -> PATCH) or correct a priority the
    AI got wrong, without needing to wait for the next AI analysis pass.
    """

    lead_status: Optional[Literal["new", "qualified", "nurturing", "won", "lost"]] = None
    priority: Optional[Literal["low", "medium", "high", "urgent"]] = None
