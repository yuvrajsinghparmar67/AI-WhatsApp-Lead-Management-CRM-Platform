"""
Conversation + message endpoints - the API surface behind the inbox UI.

GET /conversations           -> inbox list (contact + last message preview)
GET /conversations/{id}      -> full thread (contact + all messages)
POST /conversations/{id}/messages -> agent sends a reply (goes through MessagingProvider)
"""
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.ai.providers.base import AIProvider
from app.ai.providers.factory import get_ai_provider
from app.ai.retrieval.retrieval_service import find_similar_messages
from app.api.deps import get_current_user
from app.db.session import get_db
from app.messaging.base import MessagingProvider
from app.messaging.factory import get_messaging_provider
from app.schemas.conversation import ConversationDetail, ConversationListItem
from app.schemas.message import MessageRead, OutboundMessageCreate, SuggestedReplyResponse
from app.schemas.retrieval import SimilarConversationItem
from app.services import ai_pipeline_service, conversation_service, messaging_service

router = APIRouter(prefix="/conversations", tags=["conversations"], dependencies=[Depends(get_current_user)])


@router.get("", response_model=list[ConversationListItem])
def list_conversations(db: Session = Depends(get_db)):
    rows = conversation_service.list_conversations_with_previews(db)
    return [
        ConversationListItem.model_validate(
            {
                "id": row["conversation"].id,
                "status": row["conversation"].status,
                "intent": row["conversation"].intent,
                "ai_summary": row["conversation"].ai_summary,
                "created_at": row["conversation"].created_at,
                "updated_at": row["conversation"].updated_at,
                "contact": row["conversation"].contact,
                "last_message": row["last_message"],
            }
        )
        for row in rows
    ]


@router.get("/{conversation_id}", response_model=ConversationDetail)
def get_conversation(conversation_id: uuid.UUID, db: Session = Depends(get_db)):
    conversation = conversation_service.get_conversation(db, conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    messages = conversation_service.list_messages(db, conversation_id)
    return ConversationDetail.model_validate(
        {
            "id": conversation.id,
            "status": conversation.status,
            "intent": conversation.intent,
            "ai_summary": conversation.ai_summary,
            "created_at": conversation.created_at,
            "updated_at": conversation.updated_at,
            "contact": conversation.contact,
            "messages": messages,
        }
    )


@router.post("/{conversation_id}/messages", response_model=MessageRead)
async def send_message(
    conversation_id: uuid.UUID,
    payload: OutboundMessageCreate,
    db: Session = Depends(get_db),
    provider: MessagingProvider = Depends(get_messaging_provider),
):
    conversation = conversation_service.get_conversation(db, conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    return await messaging_service.send_outbound_message(
        db=db,
        conversation=conversation,
        contact=conversation.contact,
        body=payload.body,
        provider=provider,
    )


@router.post("/{conversation_id}/suggest-reply", response_model=SuggestedReplyResponse)
async def suggest_reply(
    conversation_id: uuid.UUID,
    db: Session = Depends(get_db),
    ai_provider: AIProvider = Depends(get_ai_provider),
):
    """On-demand: agent clicks "Suggest reply" and gets one AI-drafted response back, grounded in similar past conversations when relevant (RAG)."""
    conversation = conversation_service.get_conversation(db, conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    messages = conversation_service.list_messages(db, conversation_id)
    if not messages:
        raise HTTPException(status_code=400, detail="Cannot suggest a reply for an empty conversation")

    try:
        suggestion, used_context_count = await ai_pipeline_service.generate_suggested_reply(
            db, conversation, messages, ai_provider
        )
    except Exception:
        raise HTTPException(status_code=502, detail="AI provider failed to generate a suggestion")

    return SuggestedReplyResponse(suggested_reply=suggestion.strip(), used_similar_conversations=used_context_count)


@router.get("/{conversation_id}/similar", response_model=list[SimilarConversationItem])
async def get_similar_conversations(
    conversation_id: uuid.UUID,
    db: Session = Depends(get_db),
    ai_provider: AIProvider = Depends(get_ai_provider),
):
    """
    Semantic search: finds past customer messages (from OTHER
    conversations) that are similar to this conversation's latest message,
    using Gemini Embedding 2. Powers the "Similar conversations" panel.
    """
    conversation = conversation_service.get_conversation(db, conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    messages = conversation_service.list_messages(db, conversation_id)
    latest_customer_message = next((m.body for m in reversed(messages) if m.direction == "inbound"), None)
    if not latest_customer_message:
        return []

    try:
        matches = await find_similar_messages(
            db=db,
            query_text=latest_customer_message,
            provider=ai_provider,
            exclude_conversation_id=conversation_id,
            top_k=5,
        )
    except Exception:
        raise HTTPException(status_code=502, detail="AI provider failed to run semantic search")

    return [
        SimilarConversationItem(
            conversation_id=match.message.conversation_id,
            contact_name=match.message.conversation.contact.display_name or match.message.conversation.contact.phone_number,
            snippet=match.message.body,
            similarity=round(match.similarity, 3),
            ai_summary=match.message.conversation.ai_summary,
        )
        for match in matches
    ]
