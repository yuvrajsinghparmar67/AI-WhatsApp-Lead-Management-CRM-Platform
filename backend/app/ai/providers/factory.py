"""
Provider factory - the single place that decides which AIProvider
implementation to instantiate, based on the AI_PROVIDER setting.

Services call get_ai_provider() and never import GeminiProvider (or any
other concrete provider) directly.
"""
from functools import lru_cache

from app.ai.providers.base import AIProvider
from app.ai.providers.gemini_provider import GeminiProvider
from app.core.config import settings


@lru_cache
def get_ai_provider() -> AIProvider:
    if settings.AI_PROVIDER == "gemini":
        return GeminiProvider()

    # Future: elif settings.AI_PROVIDER == "openai":
    #     return OpenAIProvider()

    raise ValueError(f"Unknown AI_PROVIDER: {settings.AI_PROVIDER}")
