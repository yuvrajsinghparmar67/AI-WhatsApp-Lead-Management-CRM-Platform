"""
Pydantic model for the AI pipeline's structured output.

Parsing the model's JSON response into this schema (instead of trusting a
raw dict) means a malformed or partially-hallucinated response fails
loudly and predictably here, rather than corrupting a Contact/Conversation
row downstream.
"""
from typing import Literal, Optional

from pydantic import BaseModel, Field


class ConversationAnalysis(BaseModel):
    intent: Literal["sales_inquiry", "support_request", "complaint", "general_question", "spam"]
    lead_status: Literal["new", "qualified", "nurturing", "won", "lost"]
    priority: Literal["low", "medium", "high", "urgent"]
    sentiment: Literal["positive", "neutral", "negative"]
    estimated_budget: Optional[float] = None
    confidence_score: float = Field(ge=0.0, le=1.0)
    summary: str
