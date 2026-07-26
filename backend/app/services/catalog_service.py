"""
Business logic for the product/service/pricing catalog. Every create or
update re-embeds the item (via Gemini Embedding 2) from a formatted text
representation, so semantic search always reflects the current price/
features - not what they were when the item was first added.

Like knowledge base uploads (and unlike the message pipeline), embedding
failures here are allowed to raise: an admin saving a price change needs
to know if it didn't get indexed, not have it silently stop being
searchable.
"""
import uuid

from sqlalchemy.orm import Session

from app.ai.embeddings.embedding_service import embed_text
from app.ai.providers.base import AIProvider
from app.models.catalog_item import CatalogItem
from app.schemas.catalog import CatalogItemCreate, CatalogItemUpdate

BILLING_LABELS = {"one_time": "one-time", "monthly": "/month", "yearly": "/year"}


def format_item_for_embedding(item: CatalogItem) -> str:
    """Formats an item as short plain text for embedding/search and for grounding AI replies."""
    parts = [f"{item.name} ({item.item_type})"]

    if item.price is not None:
        billing = BILLING_LABELS.get(item.billing_period, "")
        parts.append(f"Price: {item.currency} {item.price:g}{billing}")

    if item.description:
        parts.append(item.description)

    if item.features:
        parts.append("Includes: " + ", ".join(item.features))

    if not item.is_active:
        parts.append("(currently inactive / not offered)")

    return "\n".join(parts)


async def create_item(db: Session, payload: CatalogItemCreate, provider: AIProvider) -> CatalogItem:
    item = CatalogItem(id=uuid.uuid4(), **payload.model_dump())
    item.embedding = await embed_text(format_item_for_embedding(item), provider)

    db.add(item)
    db.commit()
    db.refresh(item)
    return item


async def update_item(db: Session, item: CatalogItem, payload: CatalogItemUpdate, provider: AIProvider) -> CatalogItem:
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, field, value)

    item.embedding = await embed_text(format_item_for_embedding(item), provider)

    db.commit()
    db.refresh(item)
    return item


def list_items(db: Session) -> list[CatalogItem]:
    return db.query(CatalogItem).order_by(CatalogItem.created_at.desc()).all()


def get_item(db: Session, item_id) -> CatalogItem | None:
    return db.query(CatalogItem).filter(CatalogItem.id == item_id).first()


def delete_item(db: Session, item: CatalogItem) -> None:
    db.delete(item)
    db.commit()
