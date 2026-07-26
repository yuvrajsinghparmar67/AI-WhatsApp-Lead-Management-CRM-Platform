"""
Business logic for the Business Rules stage of the pipeline.

get_active_guardrails() feeds the "Business Rules" block of the
suggested-reply prompt (Knowledge Retrieval -> Business Rules -> Gemini).
apply_automation_rules() runs deterministically after the AI's own
analysis, so an admin's explicit policy can override or extend what the
model inferred - unlike every other AI-derived field, a rule match here
is not a guess, so it always wins over the AI's own value for that field.
"""
import uuid

from sqlalchemy.orm import Session

from app.ai.schemas import ConversationAnalysis
from app.models.business_rule import BusinessRule
from app.models.contact import Contact
from app.schemas.business_rule import BusinessRuleCreate, BusinessRuleUpdate


def create_rule(db: Session, payload: BusinessRuleCreate) -> BusinessRule:
    rule = BusinessRule(id=uuid.uuid4(), **payload.model_dump())
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return rule


def update_rule(db: Session, rule: BusinessRule, payload: BusinessRuleUpdate) -> BusinessRule:
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(rule, field, value)
    db.commit()
    db.refresh(rule)
    return rule


def list_rules(db: Session) -> list[BusinessRule]:
    return db.query(BusinessRule).order_by(BusinessRule.created_at.desc()).all()


def get_rule(db: Session, rule_id) -> BusinessRule | None:
    return db.query(BusinessRule).filter(BusinessRule.id == rule_id).first()


def delete_rule(db: Session, rule: BusinessRule) -> None:
    db.delete(rule)
    db.commit()


def get_active_guardrails(db: Session) -> list[str]:
    rules = (
        db.query(BusinessRule)
        .filter(BusinessRule.rule_type == "guardrail", BusinessRule.is_active.is_(True))
        .all()
    )
    return [rule.guardrail_text for rule in rules if rule.guardrail_text]


def apply_automation_rules(db: Session, contact: Contact, analysis: ConversationAnalysis) -> None:
    """
    Evaluates every active automation rule against the AI's just-computed
    analysis (intent/sentiment/priority) and, for each match, sets the
    configured field on the contact - overriding whatever the AI itself
    set for that field a moment earlier. Order matters: later-matching
    rules win if two rules target the same field, so rules are evaluated
    oldest-first (created_at asc) for predictable, stable behavior.
    """
    rules = (
        db.query(BusinessRule)
        .filter(BusinessRule.rule_type == "automation", BusinessRule.is_active.is_(True))
        .order_by(BusinessRule.created_at.asc())
        .all()
    )

    analysis_values = {
        "intent": analysis.intent,
        "sentiment": analysis.sentiment,
        "priority": analysis.priority,
    }

    for rule in rules:
        actual_value = analysis_values.get(rule.trigger_field)
        if actual_value == rule.trigger_value:
            setattr(contact, rule.action_field, rule.action_value)
