"""Prompt Settings endpoints - list the editable prompts and update/reset one by key."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import require_admin
from app.db.session import get_db
from app.schemas.prompt_template import PromptTemplateRead, PromptTemplateUpdate
from app.services import prompt_settings_service

router = APIRouter(prefix="/prompt-settings", tags=["prompt-settings"], dependencies=[Depends(require_admin)])


@router.get("", response_model=list[PromptTemplateRead])
def list_prompts(db: Session = Depends(get_db)):
    return prompt_settings_service.list_prompts(db)


@router.put("/{key}", response_model=PromptTemplateRead)
def update_prompt(key: str, payload: PromptTemplateUpdate, db: Session = Depends(get_db)):
    if key not in prompt_settings_service.PROMPT_REGISTRY:
        raise HTTPException(status_code=404, detail="Unknown prompt key")
    return prompt_settings_service.update_prompt(db, key, payload.custom_text)
