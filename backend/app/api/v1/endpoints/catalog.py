"""Product/service/pricing catalog endpoints."""
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.ai.providers.base import AIProvider
from app.ai.providers.factory import get_ai_provider
from app.api.deps import require_admin
from app.db.session import get_db
from app.schemas.catalog import CatalogItemCreate, CatalogItemRead, CatalogItemUpdate
from app.services import catalog_service

router = APIRouter(prefix="/catalog", tags=["catalog"], dependencies=[Depends(require_admin)])


@router.get("", response_model=list[CatalogItemRead])
def list_items(db: Session = Depends(get_db)):
    return catalog_service.list_items(db)


@router.post("", response_model=CatalogItemRead, status_code=201)
async def create_item(
    payload: CatalogItemCreate,
    db: Session = Depends(get_db),
    ai_provider: AIProvider = Depends(get_ai_provider),
):
    try:
        return await catalog_service.create_item(db, payload, ai_provider)
    except Exception:
        raise HTTPException(status_code=502, detail="Failed to save this item - check your GEMINI_API_KEY and try again.")


@router.patch("/{item_id}", response_model=CatalogItemRead)
async def update_item(
    item_id: uuid.UUID,
    payload: CatalogItemUpdate,
    db: Session = Depends(get_db),
    ai_provider: AIProvider = Depends(get_ai_provider),
):
    item = catalog_service.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    try:
        return await catalog_service.update_item(db, item, payload, ai_provider)
    except Exception:
        raise HTTPException(status_code=502, detail="Failed to save this item - check your GEMINI_API_KEY and try again.")


@router.delete("/{item_id}", status_code=204)
def delete_item(item_id: uuid.UUID, db: Session = Depends(get_db)):
    item = catalog_service.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    catalog_service.delete_item(db, item)
