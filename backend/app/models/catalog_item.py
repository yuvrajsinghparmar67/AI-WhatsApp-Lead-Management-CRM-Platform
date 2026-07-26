"""
CatalogItem - a structured product or service the business sells, with
pricing. Products/Services/Pricing were requested as three separate admin
areas, but modeled here as one entity: pricing without an item doesn't
mean anything on its own, and a product/service without a price is just
missing a field, not a different kind of thing. The Admin Portal surfaces
this as one "Products, Services & Pricing" section rather than three
near-duplicate list pages.

Like Messages and KnowledgeBaseChunks, each item carries an embedding so
it's searchable by the same RAG pattern - this is what lets a suggested
reply answer "how much is X" with the actual configured price instead of
declining to guess.
"""
import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import ARRAY, Boolean, DateTime, Float, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.db.base import Base


class CatalogItem(Base):
    __tablename__ = "catalog_items"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    item_type: Mapped[str] = mapped_column(String(16), nullable=False)  # "product" or "service"
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    features: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)

    price: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    currency: Mapped[str] = mapped_column(String(8), default="USD")
    billing_period: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)  # "one_time", "monthly", "yearly"

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Embedding of the formatted item (name + price + features + description)
    # for semantic search - see app/services/catalog_service.py.
    embedding: Mapped[Optional[list[float]]] = mapped_column(ARRAY(Float), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
