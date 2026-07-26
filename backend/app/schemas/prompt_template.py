"""Pydantic schemas for admin-editable prompt templates."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PromptTemplateRead(BaseModel):
    key: str
    label: str
    default_text: str
    custom_text: Optional[str] = None
    effective_text: str
    is_custom: bool
    updated_at: Optional[datetime] = None


class PromptTemplateUpdate(BaseModel):
    """Empty/None custom_text resets the prompt back to the code default."""
    custom_text: Optional[str] = None
