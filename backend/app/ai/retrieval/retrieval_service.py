"""
Semantic search over past customer messages using Gemini Embedding 2 -
powers both "similar conversation" lookups in the UI and the context fed
into RAG-grounded suggested replies.

Implemented as brute-force cosine similarity over every embedded inbound
message. That's fine at demo/portfolio scale (hundreds to low thousands of
messages) and keeps the stack to plain PostgreSQL. The documented upgrade
path at real scale is pgvector, which pushes this same similarity search
into an indexed ANN query in Postgres instead of Python - only this file
would need to change, since everything else already depends on this
module's functions rather than on how the search is implemented.
"""
from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.ai.providers.base import AIProvider
from app.ai.retrieval.similarity import cosine_similarity
from app.models.catalog_item import CatalogItem
from app.models.faq import FAQ
from app.models.knowledge_base import KnowledgeBaseChunk
from app.models.message import Message


@dataclass
class SimilarMessageMatch:
    message: Message
    similarity: float


@dataclass
class SimilarKnowledgeMatch:
    chunk: KnowledgeBaseChunk
    similarity: float


@dataclass
class SimilarCatalogMatch:
    item: CatalogItem
    similarity: float


@dataclass
class SimilarFAQMatch:
    faq: FAQ
    similarity: float


async def find_similar_messages(
    db: Session,
    query_text: str,
    provider: AIProvider,
    exclude_conversation_id=None,
    top_k: int = 3,
    min_similarity: float = 0.55,
) -> list[SimilarMessageMatch]:
    """
    Embeds query_text and returns the top_k most semantically similar past
    inbound customer messages (optionally excluding the current
    conversation), above a minimum similarity threshold so unrelated
    conversations don't get pulled in as "context" just to fill top_k.
    """
    query_embedding = await provider.generate_embedding(query_text)

    candidates = (
        db.query(Message)
        .filter(Message.direction == "inbound", Message.embedding.isnot(None))
        .all()
    )

    matches: list[SimilarMessageMatch] = []
    for message in candidates:
        if exclude_conversation_id and message.conversation_id == exclude_conversation_id:
            continue

        similarity = cosine_similarity(query_embedding, message.embedding)
        if similarity >= min_similarity:
            matches.append(SimilarMessageMatch(message=message, similarity=similarity))

    matches.sort(key=lambda match: match.similarity, reverse=True)
    return matches[:top_k]


async def find_similar_knowledge_chunks(
    db: Session,
    query_text: str,
    provider: AIProvider,
    top_k: int = 3,
    min_similarity: float = 0.5,
) -> list[SimilarKnowledgeMatch]:
    """
    Semantic search over the knowledge base (company info documents,
    pricing plans, uploaded PDFs/DOCX/TXT) - this is what lets a suggested
    reply confidently answer "how much is X" or "what are your hours"
    instead of declining to guess.
    """
    query_embedding = await provider.generate_embedding(query_text)

    candidates = db.query(KnowledgeBaseChunk).filter(KnowledgeBaseChunk.embedding.isnot(None)).all()

    matches = [
        SimilarKnowledgeMatch(chunk=chunk, similarity=cosine_similarity(query_embedding, chunk.embedding))
        for chunk in candidates
    ]
    matches = [m for m in matches if m.similarity >= min_similarity]
    matches.sort(key=lambda m: m.similarity, reverse=True)
    return matches[:top_k]


async def find_similar_catalog_items(
    db: Session,
    query_text: str,
    provider: AIProvider,
    top_k: int = 3,
    min_similarity: float = 0.5,
) -> list[SimilarCatalogMatch]:
    """
    Semantic search over active products/services - lets a suggested reply
    answer pricing/plan questions ("how much is X", "what's included in Y")
    with the actual configured price instead of declining to guess.
    """
    query_embedding = await provider.generate_embedding(query_text)

    candidates = (
        db.query(CatalogItem)
        .filter(CatalogItem.embedding.isnot(None), CatalogItem.is_active.is_(True))
        .all()
    )

    matches = [
        SimilarCatalogMatch(item=item, similarity=cosine_similarity(query_embedding, item.embedding))
        for item in candidates
    ]
    matches = [m for m in matches if m.similarity >= min_similarity]
    matches.sort(key=lambda m: m.similarity, reverse=True)
    return matches[:top_k]


async def find_similar_faqs(
    db: Session,
    query_text: str,
    provider: AIProvider,
    top_k: int = 3,
    min_similarity: float = 0.55,
) -> list[SimilarFAQMatch]:
    """Semantic search over active FAQs - matches however the customer actually phrases a question."""
    query_embedding = await provider.generate_embedding(query_text)

    candidates = db.query(FAQ).filter(FAQ.embedding.isnot(None), FAQ.is_active.is_(True)).all()

    matches = [
        SimilarFAQMatch(faq=faq, similarity=cosine_similarity(query_embedding, faq.embedding))
        for faq in candidates
    ]
    matches = [m for m in matches if m.similarity >= min_similarity]
    matches.sort(key=lambda m: m.similarity, reverse=True)
    return matches[:top_k]
