"""
Business logic for Follow-up Rules - the automated re-engagement stage
that fires when a conversation goes quiet, rather than in reaction to an
inbound message like every other pipeline stage.

rule_matches_conversation() and render_message() are deliberately pure
(no DB access) so they can be unit tested directly, the same pattern
user_service.py uses for its self-modification guard. run_due_follow_ups()
is the only function that touches the database or the messaging
provider - it's what both the scheduler job and the admin's manual
"Run now" button call.
"""
import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.messaging.base import MessagingProvider, OutboundMessage
from app.models.contact import Contact
from app.models.conversation import Conversation
from app.models.follow_up_log import FollowUpLog
from app.models.follow_up_rule import FollowUpRule
from app.models.message import Message
from app.schemas.follow_up_rule import FollowUpRuleCreate, FollowUpRuleUpdate

CLOSED_LEAD_STATUSES = ("won", "lost")


# --- CRUD -------------------------------------------------------------

def create_rule(db: Session, payload: FollowUpRuleCreate) -> FollowUpRule:
    rule = FollowUpRule(id=uuid.uuid4(), **payload.model_dump())
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return rule


def update_rule(db: Session, rule: FollowUpRule, payload: FollowUpRuleUpdate) -> FollowUpRule:
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(rule, field, value)
    db.commit()
    db.refresh(rule)
    return rule


def list_rules(db: Session) -> list[FollowUpRule]:
    return db.query(FollowUpRule).order_by(FollowUpRule.created_at.desc()).all()


def get_rule(db: Session, rule_id) -> FollowUpRule | None:
    return db.query(FollowUpRule).filter(FollowUpRule.id == rule_id).first()


def delete_rule(db: Session, rule: FollowUpRule) -> None:
    db.delete(rule)
    db.commit()


# --- Matching / rendering (pure - no DB) -------------------------------

def rule_matches_conversation(
    rule: FollowUpRule,
    *,
    contact_lead_status: str,
    last_message_direction: str,
    hours_since_last_message: float,
) -> bool:
    """
    A conversation is due for this rule's follow-up when:
      - the rule is active
      - the most recent message in the conversation is inbound (from the
        customer) and still unanswered - any outbound message, including a
        previous follow-up, resets the clock
      - the contact isn't already Won or Lost - a closed deal doesn't need chasing
      - the contact's lead_status matches the rule's filter, if one is set
      - it's been idle at least `idle_hours`
    """
    if not rule.is_active:
        return False
    if last_message_direction != "inbound":
        return False
    if contact_lead_status in CLOSED_LEAD_STATUSES:
        return False
    if rule.lead_status_filter and contact_lead_status != rule.lead_status_filter:
        return False
    if hours_since_last_message < rule.idle_hours:
        return False
    return True


def render_message(rule: FollowUpRule, contact: Contact) -> str:
    """Fills in {display_name}; falls back to the raw template if it's malformed."""
    name = contact.display_name or "there"
    try:
        return rule.message_template.format(display_name=name)
    except (KeyError, IndexError):
        return rule.message_template


# --- Orchestration (the scheduler's job body) --------------------------

async def run_due_follow_ups(db: Session, provider: MessagingProvider) -> list[FollowUpLog]:
    """
    For every active rule, finds open conversations that are due, sends
    the rendered follow-up through the MessagingProvider, and writes the
    outbound Message + a FollowUpLog. A FollowUpLog newer than the
    conversation's last inbound message means that quiet period has
    already been chased, so a conversation is never double-messaged by
    the same rule while waiting for a reply.
    """
    now = datetime.now(timezone.utc)
    sent: list[FollowUpLog] = []

    active_rules = db.query(FollowUpRule).filter(FollowUpRule.is_active.is_(True)).all()
    if not active_rules:
        return sent

    open_conversations = db.query(Conversation).filter(Conversation.status == "open").all()

    for conversation in open_conversations:
        last_message = (
            db.query(Message)
            .filter(Message.conversation_id == conversation.id)
            .order_by(Message.created_at.desc())
            .first()
        )
        if last_message is None:
            continue

        hours_idle = (now - last_message.created_at).total_seconds() / 3600
        contact = db.query(Contact).filter(Contact.id == conversation.contact_id).first()
        if contact is None:
            continue

        for rule in active_rules:
            if not rule_matches_conversation(
                rule,
                contact_lead_status=contact.lead_status,
                last_message_direction=last_message.direction,
                hours_since_last_message=hours_idle,
            ):
                continue

            already_sent = (
                db.query(FollowUpLog)
                .filter(
                    FollowUpLog.rule_id == rule.id,
                    FollowUpLog.conversation_id == conversation.id,
                    FollowUpLog.sent_at >= last_message.created_at,
                )
                .first()
            )
            if already_sent:
                continue

            body = render_message(rule, contact)
            await provider.send_message(OutboundMessage(to_phone_number=contact.phone_number, body=body))

            db.add(Message(
                conversation_id=conversation.id,
                direction="outbound",
                sender_type="ai",
                body=body,
            ))
            log = FollowUpLog(
                rule_id=rule.id,
                conversation_id=conversation.id,
                contact_id=contact.id,
                message_body=body,
            )
            db.add(log)
            db.commit()
            db.refresh(log)
            sent.append(log)

    return sent


def serialize_log(log: FollowUpLog) -> dict:
    return {
        "id": log.id,
        "rule_id": log.rule_id,
        "rule_name": log.rule.name if log.rule else None,
        "contact_id": log.contact_id,
        "contact_display_name": log.contact.display_name if log.contact else None,
        "contact_phone_number": log.contact.phone_number if log.contact else None,
        "conversation_id": log.conversation_id,
        "sent_at": log.sent_at,
        "message_body": log.message_body,
    }


def list_recent_logs(db: Session, limit: int = 25) -> list[dict]:
    logs = db.query(FollowUpLog).order_by(FollowUpLog.sent_at.desc()).limit(limit).all()
    return [serialize_log(log) for log in logs]
