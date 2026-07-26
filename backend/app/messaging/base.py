"""
MessagingProvider - the abstract contract every messaging channel must
implement.

The rest of the application (CRM logic, API routes, AI pipeline) only ever
talks to this interface, never to a concrete provider. That's what lets us
ship with SimulatedWhatsAppProvider today and swap in a real
WhatsAppBusinessProvider later by changing one line of config
(MESSAGING_PROVIDER in .env) - no CRM code changes.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime


@dataclass
class OutboundMessage:
    to_phone_number: str
    body: str


@dataclass
class DeliveryResult:
    provider_message_id: str
    status: str  # "sent", "delivered", "failed"
    sent_at: datetime


class MessagingProvider(ABC):
    """Every messaging channel (simulated, WhatsApp Business API, etc.) implements this."""

    @abstractmethod
    async def send_message(self, message: OutboundMessage) -> DeliveryResult:
        """Send a message to a contact and return a delivery result."""
        raise NotImplementedError

    @abstractmethod
    async def health_check(self) -> bool:
        """Return True if the provider is reachable/configured correctly."""
        raise NotImplementedError
