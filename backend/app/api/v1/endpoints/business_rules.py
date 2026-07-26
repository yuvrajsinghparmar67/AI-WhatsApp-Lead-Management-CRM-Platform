"""Business rule endpoints - guardrails and automation rules."""
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import require_admin
from app.db.session import get_db
from app.schemas.business_rule import BusinessRuleCreate, BusinessRuleRead, BusinessRuleUpdate
from app.services import business_rule_service

router = APIRouter(prefix="/business-rules", tags=["business-rules"], dependencies=[Depends(require_admin)])


@router.get("", response_model=list[BusinessRuleRead])
def list_rules(db: Session = Depends(get_db)):
    return business_rule_service.list_rules(db)


@router.post("", response_model=BusinessRuleRead, status_code=201)
def create_rule(payload: BusinessRuleCreate, db: Session = Depends(get_db)):
    return business_rule_service.create_rule(db, payload)


@router.patch("/{rule_id}", response_model=BusinessRuleRead)
def update_rule(rule_id: uuid.UUID, payload: BusinessRuleUpdate, db: Session = Depends(get_db)):
    rule = business_rule_service.get_rule(db, rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    return business_rule_service.update_rule(db, rule, payload)


@router.delete("/{rule_id}", status_code=204)
def delete_rule(rule_id: uuid.UUID, db: Session = Depends(get_db)):
    rule = business_rule_service.get_rule(db, rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    business_rule_service.delete_rule(db, rule)
