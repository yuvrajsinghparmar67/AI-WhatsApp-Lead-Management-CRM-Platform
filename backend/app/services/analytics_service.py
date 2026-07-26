"""
Aggregate queries powering the analytics dashboard: lead funnel, priority
and sentiment breakdowns, average first-response time, and a daily
message-volume trend.

Kept as plain, readable Python/SQLAlchemy rather than a raw-SQL reporting
layer - at this project's scale that's the right tradeoff, and every
function here is small enough to swap for a materialized view later
without touching the API layer.
"""
from collections import defaultdict
from datetime import datetime, timedelta, timezone

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.contact import Contact
from app.models.conversation import Conversation
from app.models.message import Message

LEAD_STATUSES = ["new", "qualified", "nurturing", "won", "lost"]
PRIORITIES = ["low", "medium", "high", "urgent"]
SENTIMENTS = ["positive", "neutral", "negative"]


def get_lead_funnel(db: Session) -> dict[str, int]:
    counts = dict(db.query(Contact.lead_status, func.count(Contact.id)).group_by(Contact.lead_status).all())
    return {status: counts.get(status, 0) for status in LEAD_STATUSES}


def get_priority_breakdown(db: Session) -> dict[str, int]:
    counts = dict(db.query(Contact.priority, func.count(Contact.id)).group_by(Contact.priority).all())
    return {priority: counts.get(priority, 0) for priority in PRIORITIES}


def get_sentiment_breakdown(db: Session) -> dict[str, int]:
    counts = dict(
        db.query(Contact.sentiment, func.count(Contact.id))
        .filter(Contact.sentiment.isnot(None))
        .group_by(Contact.sentiment)
        .all()
    )
    return {sentiment: counts.get(sentiment, 0) for sentiment in SENTIMENTS}


def get_avg_response_time_seconds(db: Session) -> float | None:
    """
    For every conversation, finds each inbound message and the next
    outbound message that followed it, and averages the gap - a simple
    proxy for "how fast does the business respond to a customer".

    Computed in Python over all messages ordered by conversation + time;
    fine at this project's scale, and easy to push into SQL with a window
    function later if message volume grows.
    """
    messages = db.query(Message).order_by(Message.conversation_id, Message.created_at.asc()).all()

    by_conversation: dict = defaultdict(list)
    for message in messages:
        by_conversation[message.conversation_id].append(message)

    gaps: list[float] = []
    for conv_messages in by_conversation.values():
        pending_inbound_at = None
        for message in conv_messages:
            if message.direction == "inbound":
                pending_inbound_at = message.created_at
            elif message.direction == "outbound" and pending_inbound_at is not None:
                gaps.append((message.created_at - pending_inbound_at).total_seconds())
                pending_inbound_at = None

    if not gaps:
        return None
    return sum(gaps) / len(gaps)


def get_messages_per_day(db: Session, days: int = 14) -> list[dict]:
    since = datetime.now(timezone.utc) - timedelta(days=days)
    messages = db.query(Message).filter(Message.created_at >= since).all()

    daily: dict[str, dict[str, int]] = defaultdict(lambda: {"inbound": 0, "outbound": 0})
    for message in messages:
        date_key = message.created_at.date().isoformat()
        daily[date_key][message.direction] += 1

    # Fill in every day in the range (including zero-message days) so the
    # frontend trend line doesn't have gaps.
    result = []
    for offset in range(days - 1, -1, -1):
        date_key = (datetime.now(timezone.utc).date() - timedelta(days=offset)).isoformat()
        counts = daily.get(date_key, {"inbound": 0, "outbound": 0})
        result.append({"date": date_key, "inbound": counts["inbound"], "outbound": counts["outbound"]})

    return result


def get_overview(db: Session) -> dict:
    return {
        "total_contacts": db.query(func.count(Contact.id)).scalar() or 0,
        "total_conversations": db.query(func.count(Conversation.id)).scalar() or 0,
        "lead_funnel": get_lead_funnel(db),
        "priority_breakdown": get_priority_breakdown(db),
        "sentiment_breakdown": get_sentiment_breakdown(db),
        "avg_response_time_seconds": get_avg_response_time_seconds(db),
        "messages_per_day": get_messages_per_day(db),
    }
