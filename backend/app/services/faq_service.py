"""
Business logic for FAQs. Like the catalog, every create/update re-embeds
the FAQ (question+answer together) so semantic search stays current and
matches however a customer actually phrases the question - not just the
exact wording the admin typed.
"""
import uuid

from sqlalchemy.orm import Session

from app.ai.embeddings.embedding_service import embed_text
from app.ai.providers.base import AIProvider
from app.models.faq import FAQ
from app.schemas.faq import FAQCreate, FAQUpdate


def format_faq_for_embedding(faq: FAQ) -> str:
    return f"Q: {faq.question}\nA: {faq.answer}"


async def create_faq(db: Session, payload: FAQCreate, provider: AIProvider) -> FAQ:
    faq = FAQ(id=uuid.uuid4(), **payload.model_dump())
    faq.embedding = await embed_text(format_faq_for_embedding(faq), provider)

    db.add(faq)
    db.commit()
    db.refresh(faq)
    return faq


async def update_faq(db: Session, faq: FAQ, payload: FAQUpdate, provider: AIProvider) -> FAQ:
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(faq, field, value)

    faq.embedding = await embed_text(format_faq_for_embedding(faq), provider)

    db.commit()
    db.refresh(faq)
    return faq


def list_faqs(db: Session) -> list[FAQ]:
    return db.query(FAQ).order_by(FAQ.created_at.desc()).all()


def get_faq(db: Session, faq_id) -> FAQ | None:
    return db.query(FAQ).filter(FAQ.id == faq_id).first()


def delete_faq(db: Session, faq: FAQ) -> None:
    db.delete(faq)
    db.commit()
