"""Business logic for the singleton AI Settings row - same get-or-create pattern as company_service."""
import uuid

from sqlalchemy.orm import Session

from app.models.ai_settings import AISettings
from app.schemas.ai_settings import AISettingsUpdate


def get_or_create_settings(db: Session) -> AISettings:
    settings = db.query(AISettings).first()
    if settings:
        return settings

    settings = AISettings(id=uuid.uuid4())
    db.add(settings)
    db.commit()
    db.refresh(settings)
    return settings


def update_settings(db: Session, updates: AISettingsUpdate) -> AISettings:
    settings = get_or_create_settings(db)

    for field, value in updates.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(settings, field, value)

    db.commit()
    db.refresh(settings)
    return settings
