"""
Thin wrapper around AIProvider.generate_embedding for message text.

Kept as its own module (rather than calling the provider directly from
services) so retrieval/analytics code depends on "embed this text" as a
concept, not on which provider produces the vector.
"""
from app.ai.providers.base import AIProvider


async def embed_text(text: str, provider: AIProvider) -> list[float]:
    return await provider.generate_embedding(text)
