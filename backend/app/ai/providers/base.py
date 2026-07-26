"""
AIProvider - the abstract contract every AI backend must implement.

Business logic (intent detection, lead qualification, summarization, etc.
- built in a later milestone) will depend only on this interface. Swapping
Gemini for OpenAI, Claude, or a local model later means writing one new
class here and changing AI_PROVIDER in .env - nothing in app/services or
app/api changes.
"""
from abc import ABC, abstractmethod
from typing import List, Optional


class AIProvider(ABC):
    @abstractmethod
    async def generate_text(
        self,
        system_prompt: str,
        user_prompt: str,
        model: Optional[str] = None,
        temperature: float = 0.7,
    ) -> str:
        """
        Send a prompt to the model and return its raw text response.
        model/temperature are optional per-call overrides - callers that
        care about admin-configured AI Settings (see
        app/services/ai_settings_service.py) pass them explicitly;
        callers that don't just get the provider's own default.
        """
        raise NotImplementedError

    @abstractmethod
    async def generate_embedding(self, text: str) -> List[float]:
        """Return a vector embedding for the given text."""
        raise NotImplementedError
