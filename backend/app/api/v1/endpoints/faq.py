"""FAQ endpoints."""
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.ai.providers.base import AIProvider
from app.ai.providers.factory import get_ai_provider
from app.api.deps import require_admin
from app.db.session import get_db
from app.schemas.faq import FAQCreate, FAQRead, FAQUpdate
from app.services import faq_service

router = APIRouter(prefix="/faqs", tags=["faqs"], dependencies=[Depends(require_admin)])


@router.get("", response_model=list[FAQRead])
def list_faqs(db: Session = Depends(get_db)):
    return faq_service.list_faqs(db)


@router.post("", response_model=FAQRead, status_code=201)
async def create_faq(
    payload: FAQCreate,
    db: Session = Depends(get_db),
    ai_provider: AIProvider = Depends(get_ai_provider),
):
    try:
        return await faq_service.create_faq(db, payload, ai_provider)
    except Exception:
        raise HTTPException(status_code=502, detail="Failed to save this FAQ - check your GEMINI_API_KEY and try again.")


@router.patch("/{faq_id}", response_model=FAQRead)
async def update_faq(
    faq_id: uuid.UUID,
    payload: FAQUpdate,
    db: Session = Depends(get_db),
    ai_provider: AIProvider = Depends(get_ai_provider),
):
    faq = faq_service.get_faq(db, faq_id)
    if not faq:
        raise HTTPException(status_code=404, detail="FAQ not found")

    try:
        return await faq_service.update_faq(db, faq, payload, ai_provider)
    except Exception:
        raise HTTPException(status_code=502, detail="Failed to save this FAQ - check your GEMINI_API_KEY and try again.")


@router.delete("/{faq_id}", status_code=204)
def delete_faq(faq_id: uuid.UUID, db: Session = Depends(get_db)):
    faq = faq_service.get_faq(db, faq_id)
    if not faq:
        raise HTTPException(status_code=404, detail="FAQ not found")
    faq_service.delete_faq(db, faq)
