"""
GeminiProvider - concrete AIProvider implementation using Google's
official GenAI SDK (Gemini 3.5 Flash for text, Gemini Embedding 2 for
vectors).

This is the ONLY file in the codebase that imports the google-genai SDK.
Every AI feature (intent detection, summarization, RAG, etc.) is built on
top of the AIProvider interface, so this file could be deleted and
replaced with an OpenAIProvider without touching anything upstream.
"""
from typing import List, Optional

from google import genai

from app.ai.providers.base import AIProvider
from app.core.config import settings


class GeminiProvider(AIProvider):
    def __init__(self) -> None:
        self._client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self._default_chat_model = settings.GEMINI_CHAT_MODEL
        self._embedding_model = settings.GEMINI_EMBEDDING_MODEL

    async def generate_text(
        self,
        system_prompt: str,
        user_prompt: str,
        model: Optional[str] = None,
        temperature: float = 0.7,
    ) -> str:
        response = self._client.models.generate_content(
            model=model or self._default_chat_model,
            contents=user_prompt,
            config={"system_instruction": system_prompt, "temperature": temperature},
        )
        return response.text

    async def generate_embedding(self, text: str) -> List[float]:
        response = self._client.models.embed_content(
            model=self._embedding_model,
            contents=text,
        )
        return response.embeddings[0].values
