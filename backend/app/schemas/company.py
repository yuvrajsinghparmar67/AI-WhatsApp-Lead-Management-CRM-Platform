"""Pydantic schemas for the singleton Company profile."""
import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class BusinessHoursDay(BaseModel):
    day: str
    closed: bool = False
    open: Optional[str] = None   # "09:00"
    close: Optional[str] = None  # "18:00"


class CompanyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    business_name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    business_hours: list[BusinessHoursDay] = []
    updated_at: datetime


class CompanyUpdate(BaseModel):
    business_name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    business_hours: Optional[list[BusinessHoursDay]] = None
