"""
Orchestrates messaging: this is where the CRM's domain logic (get-or-create
contact/conversation, persist a Message row) meets the MessagingProvider
abstraction (actually "sending" the outbound text) and the AI pipeline
(analyzing the conversation whenever a new inbound message arrives).
Routes call into this service; they never touch MessagingProvider, the AI
pipeline, or the ORM models directly.
"""
from sqlalchemy.orm import Session

from app.ai.providers.base import AIProvider
from app.messaging.base import MessagingProvider, OutboundMessage
from app.models.contact import Contact
from app.models.conversation import Conversation
from app.models.message import Message
from app.services import ai_pipeline_service
from app.services.contact_service import get_or_create_contact
from app.services.conversation_service import get_or_create_open_conversation, list_messages


async def send_outbound_message(
    db: Session,
    conversation: Conversation,
    contact: Contact,
    body: str,
    provider: MessagingProvider,
) -> Message:
    """An agent (or, in a later milestone, the AI) replies inside a conversation."""
    await provider.send_message(OutboundMessage(to_phone_number=contact.phone_number, body=body))

    message = Message(
        conversation_id=conversation.id,
        direction="outbound",
        sender_type="agent",
        body=body,
    )
    db.add(message)
    conversation.status = "open"
    db.commit()
    db.refresh(message)
    return message


async def receive_inbound_message(
    db: Session,
    phone_number: str,
    display_name: str | None,
    body: str,
    ai_provider: AIProvider,
) -> Message:
    """
    Simulates (or, later, actually handles) an inbound customer message:
    find-or-create the contact, find-or-create their open conversation,
    persist the message, then run the AI pipeline against the updated
    transcript so the contact's lead_status/priority/sentiment/etc. and the
    conversation's intent/summary stay current.

    The AI step runs synchronously (awaited before this returns) rather
    than as a background task, which keeps the demo simple and avoids
    managing a second DB session - the tradeoff is the simulate/inbound
    call takes an extra second or two for the AI round-trip. Moving this to
    a background task or a queue is the natural next step once real
    message volume matters.
    """
    contact = get_or_create_contact(db, phone_number=phone_number, display_name=display_name)
    conversation = get_or_create_open_conversation(db, contact)

    message = Message(
        conversation_id=conversation.id,
        direction="inbound",
        sender_type="contact",
        body=body,
    )
    db.add(message)
    db.commit()
    db.refresh(message)

    all_messages = list_messages(db, conversation.id)
    await ai_pipeline_service.embed_inbound_message(db, message, ai_provider)
    await ai_pipeline_service.analyze_conversation(db, conversation, all_messages, ai_provider)

    return message
