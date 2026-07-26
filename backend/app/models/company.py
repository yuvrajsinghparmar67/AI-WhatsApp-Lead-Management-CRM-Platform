"""
Company model - a SINGLETON row holding the business's own profile (name,
contact info, hours). Not per-user, not per-conversation: one business
runs one instance of this CRM, so there's exactly one row, maintained via
GET/PUT /company rather than a full CRUD resource.

business_hours is stored as a JSON string in a plain Text column (rather
than a real JSONB column) to keep the schema simple for a single small
structure - the natural upgrade if this grew more complex would be a real
JSONB column or a separate BusinessHours table.
"""
import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.db.base import Base


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    website: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    business_hours: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string - see module docstring

    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
