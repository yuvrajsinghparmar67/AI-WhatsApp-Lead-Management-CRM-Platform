"""AI Settings endpoint - a singleton resource, not a list."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import require_admin
from app.db.session import get_db
from app.schemas.ai_settings import AISettingsRead, AISettingsUpdate
from app.services import ai_settings_service

router = APIRouter(prefix="/ai-settings", tags=["ai-settings"], dependencies=[Depends(require_admin)])


@router.get("", response_model=AISettingsRead)
def get_settings(db: Session = Depends(get_db)):
    return ai_settings_service.get_or_create_settings(db)


@router.put("", response_model=AISettingsRead)
def update_settings(payload: AISettingsUpdate, db: Session = Depends(get_db)):
    return ai_settings_service.update_settings(db, payload)
