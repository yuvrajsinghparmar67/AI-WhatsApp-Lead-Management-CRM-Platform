"""
APScheduler wiring - the "new infra" Follow-up Rules needed. Runs the
follow-up job on a fixed interval in-process, inside the FastAPI backend
itself, via AsyncIOScheduler on the same event loop uvicorn already runs.
No separate worker service or message queue exists yet - that's a
deliberate scope call for this milestone (see README "known limitations"
for what a multi-instance deployment would need instead: an external
scheduler, e.g. Celery beat or cron, hitting a dedicated endpoint so two
backend replicas don't both fire the same rule at once).
"""
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.core.config import settings
from app.scheduler.jobs import run_follow_up_rules_job

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


def start_scheduler() -> None:
    if not settings.FOLLOW_UP_SCHEDULER_ENABLED:
        logger.info("follow_up_rules: scheduler disabled (FOLLOW_UP_SCHEDULER_ENABLED=false)")
        return

    scheduler.add_job(
        run_follow_up_rules_job,
        "interval",
        minutes=settings.FOLLOW_UP_SCHEDULER_INTERVAL_MINUTES,
        id="follow_up_rules",
        replace_existing=True,
    )
    scheduler.start()
    logger.info(
        "follow_up_rules: scheduler started (every %s minute(s))",
        settings.FOLLOW_UP_SCHEDULER_INTERVAL_MINUTES,
    )


def stop_scheduler() -> None:
    if scheduler.running:
        scheduler.shutdown(wait=False)
