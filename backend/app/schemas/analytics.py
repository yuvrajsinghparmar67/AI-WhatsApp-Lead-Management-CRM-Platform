"""Pydantic schemas for the analytics dashboard's aggregate endpoint."""
from typing import Optional

from pydantic import BaseModel


class DailyMessageCount(BaseModel):
    date: str  # ISO date, e.g. "2026-07-20"
    inbound: int
    outbound: int


class AnalyticsOverview(BaseModel):
    total_contacts: int
    total_conversations: int
    lead_funnel: dict[str, int]
    priority_breakdown: dict[str, int]
    sentiment_breakdown: dict[str, int]
    avg_response_time_seconds: Optional[float] = None
    messages_per_day: list[DailyMessageCount]
