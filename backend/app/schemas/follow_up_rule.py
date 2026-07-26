"""Pydantic schemas for Follow-up Rules and their activity log."""
import uuid
from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

LEAD_STATUSES = ("new", "qualified", "nurturing", "won", "lost")


class FollowUpRuleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    is_active: bool
    idle_hours: int
    lead_status_filter: Optional[str] = None
    message_template: str
    created_at: datetime
    updated_at: datetime


class FollowUpRuleCreate(BaseModel):
    name: str
    is_active: bool = True
    idle_hours: int = Field(gt=0, le=720)  # up to 30 days
    lead_status_filter: Optional[Literal["new", "qualified", "nurturing"]] = None
    message_template: str


class FollowUpRuleUpdate(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None
    idle_hours: Optional[int] = Field(default=None, gt=0, le=720)
    lead_status_filter: Optional[Literal["new", "qualified", "nurturing"]] = None
    message_template: Optional[str] = None


class FollowUpRuleLogRead(BaseModel):
    id: uuid.UUID
    rule_id: uuid.UUID
    rule_name: Optional[str] = None
    contact_id: uuid.UUID
    contact_display_name: Optional[str] = None
    contact_phone_number: Optional[str] = None
    conversation_id: uuid.UUID
    sent_at: datetime
    message_body: str
