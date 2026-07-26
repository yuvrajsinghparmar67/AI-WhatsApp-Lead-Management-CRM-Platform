"""
Simulator endpoint - stands in for a real WhatsApp webhook.

In production, WhatsAppBusinessProvider would receive inbound messages via
a webhook Meta calls on your server. Since we're running
SimulatedWhatsAppProvider, this endpoint is how the inbox gets populated
during development/demos: the frontend's "Simulate incoming message" panel
posts here to pretend a customer just texted in. Each call also runs the
AI pipeline, exactly as a real webhook handler would.

Deliberately left WITHOUT the app's JWT auth (unlike /contacts,
/conversations, /analytics): a real WhatsApp webhook is called by Meta's
servers, not a logged-in agent, and would authenticate via a webhook
verify token/signature instead - not a user login. That real verification
step is exactly what WhatsAppBusinessProvider would add later.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.ai.providers.base import AIProvider
from app.ai.providers.factory import get_ai_provider
from app.db.session import get_db
from app.schemas.message import InboundMessageCreate, MessageRead
from app.services import messaging_service

router = APIRouter(prefix="/simulate", tags=["simulator"])


@router.post("/inbound", response_model=MessageRead)
async def simulate_inbound_message(
    payload: InboundMessageCreate,
    db: Session = Depends(get_db),
    ai_provider: AIProvider = Depends(get_ai_provider),
):
    return await messaging_service.receive_inbound_message(
        db=db,
        phone_number=payload.phone_number,
        display_name=payload.display_name,
        body=payload.body,
        ai_provider=ai_provider,
    )
