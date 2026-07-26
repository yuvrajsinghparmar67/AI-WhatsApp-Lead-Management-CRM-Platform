"""
Follow-up rule endpoints - admin CRUD over the rules, the recent-activity
log, and a manual "run now" trigger so the scheduler's behavior can be
verified on demand instead of waiting for real idle hours to pass.
"""
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import require_admin
from app.db.session import get_db
from app.messaging.factory import get_messaging_provider
from app.schemas.follow_up_rule import (
    FollowUpRuleCreate,
    FollowUpRuleLogRead,
    FollowUpRuleRead,
    FollowUpRuleUpdate,
)
from app.services import follow_up_rule_service

router = APIRouter(prefix="/follow-up-rules", tags=["follow-up-rules"], dependencies=[Depends(require_admin)])


@router.get("", response_model=list[FollowUpRuleRead])
def list_rules(db: Session = Depends(get_db)):
    return follow_up_rule_service.list_rules(db)


@router.post("", response_model=FollowUpRuleRead, status_code=201)
def create_rule(payload: FollowUpRuleCreate, db: Session = Depends(get_db)):
    return follow_up_rule_service.create_rule(db, payload)


@router.patch("/{rule_id}", response_model=FollowUpRuleRead)
def update_rule(rule_id: uuid.UUID, payload: FollowUpRuleUpdate, db: Session = Depends(get_db)):
    rule = follow_up_rule_service.get_rule(db, rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    return follow_up_rule_service.update_rule(db, rule, payload)


@router.delete("/{rule_id}", status_code=204)
def delete_rule(rule_id: uuid.UUID, db: Session = Depends(get_db)):
    rule = follow_up_rule_service.get_rule(db, rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    follow_up_rule_service.delete_rule(db, rule)


@router.get("/logs", response_model=list[FollowUpRuleLogRead])
def list_logs(db: Session = Depends(get_db)):
    return follow_up_rule_service.list_recent_logs(db)


@router.post("/run-now", response_model=list[FollowUpRuleLogRead])
async def run_now(db: Session = Depends(get_db)):
    """Fires the same job the scheduler runs on a timer, immediately."""
    provider = get_messaging_provider()
    sent = await follow_up_rule_service.run_due_follow_ups(db, provider)
    return [follow_up_rule_service.serialize_log(log) for log in sent]
