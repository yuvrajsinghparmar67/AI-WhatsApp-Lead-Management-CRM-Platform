"""
SimulatedWhatsAppProvider - a fake WhatsApp channel that behaves like
WhatsApp Web for local development and demos.

It doesn't call any external API: it just records the outbound message and
returns a delivery result that looks like what a real provider would send
back. This lets the whole CRM (dashboard, AI pipeline, analytics) be built
and demoed end-to-end before any real WhatsApp Business API credentials
exist.
"""
import uuid
from datetime import datetime, timezone

from app.messaging.base import DeliveryResult, MessagingProvider, OutboundMessage


class SimulatedWhatsAppProvider(MessagingProvider):
    async def send_message(self, message: OutboundMessage) -> DeliveryResult:
        # In a real provider this would be an HTTP call to the WhatsApp
        # Business API. Here we simply simulate a successful send.
        return DeliveryResult(
            provider_message_id=f"sim_{uuid.uuid4().hex[:12]}",
            status="delivered",
            sent_at=datetime.now(timezone.utc),
        )

    async def health_check(self) -> bool:
        return True
