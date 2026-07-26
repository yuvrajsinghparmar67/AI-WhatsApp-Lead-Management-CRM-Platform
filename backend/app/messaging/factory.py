"""
Provider factory - the single place that decides which MessagingProvider
implementation to instantiate, based on the MESSAGING_PROVIDER setting.

Everything else in the app calls get_messaging_provider() and never
imports a concrete provider class directly.
"""
from functools import lru_cache

from app.core.config import settings
from app.messaging.base import MessagingProvider
from app.messaging.simulated_whatsapp import SimulatedWhatsAppProvider


@lru_cache
def get_messaging_provider() -> MessagingProvider:
    if settings.MESSAGING_PROVIDER == "simulated":
        return SimulatedWhatsAppProvider()

    # Future: elif settings.MESSAGING_PROVIDER == "whatsapp_business":
    #     return WhatsAppBusinessProvider()

    raise ValueError(f"Unknown MESSAGING_PROVIDER: {settings.MESSAGING_PROVIDER}")
