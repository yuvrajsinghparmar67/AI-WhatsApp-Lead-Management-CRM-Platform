"""
Orchestrates the AI pipeline: turns a conversation's message history into
a transcript, sends it to the configured AIProvider, parses the structured
result, and writes it onto the Contact/Conversation rows. Also owns the
retrieval-augmented pieces - embedding inbound messages as they arrive,
and grounding suggested replies in the knowledge base and similar past
conversations - plus applying admin-configured AI Settings (model,
temperature, on/off toggles) and Prompt Settings (editable system
prompts) to every call.

This is the only place that calls AIProvider - routes and other services
never talk to the provider directly, so the pipeline's error handling (a
bad AI response should never break the messaging flow) lives in one place.
"""
import logging

from sqlalchemy.orm import Session

from app.ai.embeddings.embedding_service import embed_text
from app.ai.prompts import conversation_analysis, suggested_reply
from app.ai.providers.base import AIProvider
from app.ai.retrieval.retrieval_service import (
    find_similar_catalog_items,
    find_similar_faqs,
    find_similar_knowledge_chunks,
    find_similar_messages,
)
from app.ai.schemas import ConversationAnalysis
from app.ai.utils import parse_json_response
from app.models.conversation import Conversation
from app.models.message import Message
from app.services import ai_settings_service, business_rule_service, company_service, prompt_settings_service
from app.services.catalog_service import format_item_for_embedding

logger = logging.getLogger(__name__)


def _build_transcript(messages: list[Message]) -> str:
    lines = []
    for message in messages:
        speaker = "Customer" if message.direction == "inbound" else "Agent"
        lines.append(f"{speaker}: {message.body}")
    return "\n".join(lines)


async def embed_inbound_message(db: Session, message: Message, provider: AIProvider) -> None:
    """
    Generates and stores a Gemini Embedding 2 vector for a newly-saved
    inbound message, so it becomes searchable for future semantic-search /
    RAG lookups. Runs regardless of the rag_enabled AI Setting - embedding
    is cheap and keeps data ready to search the moment RAG is turned back
    on, without needing a backfill. Fails soft like analyze_conversation -
    an embedding failure should never block the message from being saved.
    """
    try:
        message.embedding = await embed_text(message.body, provider)
        db.commit()
    except Exception:
        logger.exception("Failed to embed message %s; it just won't be retrievable by semantic search.", message.id)


async def analyze_conversation(db: Session, conversation: Conversation, messages: list[Message], provider: AIProvider) -> None:
    """
    Runs the full-signal analysis prompt and writes the result onto the
    conversation's contact and the conversation itself. Called after every
    inbound message - unless AI Settings has auto_analysis_enabled off,
    in which case this is a deliberate no-op (an admin-controlled pause,
    not a failure).

    Otherwise fails soft: an AI outage, a malformed response, or a
    missing API key should never prevent a customer message from being
    saved and shown in the inbox - it should just mean the AI fields stay
    stale until the next successful analysis.
    """
    if not messages:
        return

    ai_settings = ai_settings_service.get_or_create_settings(db)
    if not ai_settings.auto_analysis_enabled:
        logger.info("Auto-analysis is disabled in AI Settings; skipping for conversation %s.", conversation.id)
        return

    transcript = _build_transcript(messages)
    system_prompt = prompt_settings_service.get_effective_prompt(db, "conversation_analysis")

    try:
        raw_response = await provider.generate_text(
            system_prompt=system_prompt,
            user_prompt=conversation_analysis.build_user_prompt(transcript),
            model=ai_settings.chat_model,
            temperature=ai_settings.temperature,
        )
        parsed = parse_json_response(raw_response)
        analysis = ConversationAnalysis.model_validate(parsed)
    except Exception:
        logger.exception("AI conversation analysis failed for conversation %s; leaving prior AI fields unchanged.", conversation.id)
        return

    contact = conversation.contact
    contact.lead_status = analysis.lead_status
    contact.priority = analysis.priority
    contact.sentiment = analysis.sentiment
    contact.estimated_budget = analysis.estimated_budget
    contact.confidence_score = analysis.confidence_score

    conversation.intent = analysis.intent
    conversation.ai_summary = analysis.summary

    # Business Rules stage (automation rules): deterministic admin policy
    # applied on top of the AI's own read. A rule match is not a guess, so
    # it overrides whatever the AI itself just set for that field.
    business_rule_service.apply_automation_rules(db, contact, analysis)

    db.commit()


async def generate_suggested_reply(
    db: Session,
    conversation: Conversation,
    messages: list[Message],
    provider: AIProvider,
) -> tuple[str, int]:
    """
    On-demand: an agent clicks "Suggest reply" and gets one drafted
    response back, grounded in this conversation's transcript, business
    rules, the company's own profile/catalog/FAQs/knowledge base, AND (via
    RAG) any semantically similar past conversations. Unlike
    analyze_conversation this is not auto-triggered - it's only called
    when an agent actually wants a draft, so raising on failure (rather
    than failing soft) is correct here - the caller/UI surfaces the error.

    If AI Settings has rag_enabled off, all four embedding-search-based
    context sources (catalog/FAQs/knowledge base/similar conversations)
    are skipped - business rules and the company profile still apply,
    since those are direct lookups, not retrieval.

    Returns (suggested_text, number_of_similar_conversations_used) so the
    UI can show whether/how much past-conversation context informed the
    draft.
    """
    ai_settings = ai_settings_service.get_or_create_settings(db)
    transcript = _build_transcript(messages)

    latest_customer_message = next(
        (m.body for m in reversed(messages) if m.direction == "inbound"),
        None,
    )

    business_rules = business_rule_service.get_active_guardrails(db)
    company_profile = company_service.format_company_profile_for_ai(db)
    catalog_context = None
    faq_context = None
    company_knowledge = None
    retrieved_context = None
    used_context_count = 0

    if ai_settings.rag_enabled and latest_customer_message:
        catalog_matches = await find_similar_catalog_items(
            db=db, query_text=latest_customer_message, provider=provider, top_k=3
        )
        if catalog_matches:
            catalog_context = "\n---\n".join(format_item_for_embedding(match.item) for match in catalog_matches)

        faq_matches = await find_similar_faqs(db=db, query_text=latest_customer_message, provider=provider, top_k=3)
        if faq_matches:
            faq_context = "\n---\n".join(f"Q: {m.faq.question}\nA: {m.faq.answer}" for m in faq_matches)

        knowledge_matches = await find_similar_knowledge_chunks(
            db=db, query_text=latest_customer_message, provider=provider, top_k=3
        )
        if knowledge_matches:
            company_knowledge = "\n---\n".join(match.chunk.content for match in knowledge_matches)

        conversation_matches = await find_similar_messages(
            db=db,
            query_text=latest_customer_message,
            provider=provider,
            exclude_conversation_id=conversation.id,
            top_k=3,
        )
        if conversation_matches:
            used_context_count = len(conversation_matches)
            retrieved_context = "\n---\n".join(
                f"Customer said: {match.message.body}" for match in conversation_matches
            )

    system_prompt = prompt_settings_service.get_effective_prompt(db, "suggested_reply")

    suggestion = await provider.generate_text(
        system_prompt=system_prompt,
        user_prompt=suggested_reply.build_user_prompt(
            transcript,
            business_rules=business_rules,
            company_profile=company_profile,
            catalog_context=catalog_context,
            faq_context=faq_context,
            company_knowledge=company_knowledge,
            similar_conversations=retrieved_context,
        ),
        model=ai_settings.chat_model,
        temperature=ai_settings.temperature,
    )
    return suggestion, used_context_count
