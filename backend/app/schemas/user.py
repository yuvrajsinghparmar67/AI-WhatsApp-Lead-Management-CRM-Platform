"""Pydantic schemas for User - request/response shapes, never the ORM model itself."""
import uuid
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    full_name: str


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    is_active: bool
    role: Literal["admin", "agent"]


class UserUpdate(BaseModel):
    """Admin-only: change a teammate's role or active status. See api/deps.py::require_admin."""

    role: Optional[Literal["admin", "agent"]] = None
    is_active: Optional[bool] = None
