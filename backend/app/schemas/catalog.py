"""Pydantic schemas for the product/service/pricing catalog."""
import uuid
from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class CatalogItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    item_type: Literal["product", "service"]
    description: Optional[str] = None
    features: list[str] = []
    price: Optional[float] = None
    currency: str = "USD"
    billing_period: Optional[Literal["one_time", "monthly", "yearly"]] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime


class CatalogItemCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    item_type: Literal["product", "service"]
    description: Optional[str] = None
    features: list[str] = []
    price: Optional[float] = None
    currency: str = "USD"
    billing_period: Optional[Literal["one_time", "monthly", "yearly"]] = None
    is_active: bool = True


class CatalogItemUpdate(BaseModel):
    name: Optional[str] = None
    item_type: Optional[Literal["product", "service"]] = None
    description: Optional[str] = None
    features: Optional[list[str]] = None
    price: Optional[float] = None
    currency: Optional[str] = None
    billing_period: Optional[Literal["one_time", "monthly", "yearly"]] = None
    is_active: Optional[bool] = None
