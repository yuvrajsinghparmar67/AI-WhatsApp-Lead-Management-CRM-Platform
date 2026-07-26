"""
The recurring job the scheduler runs. Kept separate from
follow_up_rule_service so the scheduling mechanism (APScheduler) and the
domain logic (which conversations are due, what to send) stay decoupled -
this module just opens a session, delegates, and closes it.
"""
import logging

from app.db.session import SessionLocal
from app.messaging.factory import get_messaging_provider
from app.services import follow_up_rule_service

logger = logging.getLogger(__name__)


async def run_follow_up_rules_job() -> None:
    db = SessionLocal()
    try:
        provider = get_messaging_provider()
        sent = await follow_up_rule_service.run_due_follow_ups(db, provider)
        if sent:
            logger.info("follow_up_rules: sent %d follow-up message(s)", len(sent))
    except Exception:
        # A single failed tick (e.g. a transient DB blip) should never take
        # the scheduler down - it just tries again on the next interval.
        logger.exception("follow_up_rules: scheduled run failed")
    finally:
        db.close()
