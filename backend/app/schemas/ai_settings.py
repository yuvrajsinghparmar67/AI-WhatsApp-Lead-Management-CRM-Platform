"""Pydantic schemas for the singleton AI Settings."""
import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class AISettingsRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    chat_model: str
    temperature: float
    auto_analysis_enabled: bool
    rag_enabled: bool
    updated_at: datetime


class AISettingsUpdate(BaseModel):
    chat_model: Optional[str] = None
    temperature: Optional[float] = Field(default=None, ge=0.0, le=2.0)
    auto_analysis_enabled: Optional[bool] = None
    rag_enabled: Optional[bool] = None
