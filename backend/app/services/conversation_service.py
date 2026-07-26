"""
Business logic for Conversations, including assembling the inbox list
(each conversation + its contact + a preview of the latest message).
"""
from typing import Optional

from sqlalchemy.orm import Session

from app.models.contact import Contact
from app.models.conversation import Conversation
from app.models.message import Message


def get_or_create_open_conversation(db: Session, contact: Contact) -> Conversation:
    """
    Returns the contact's currently open conversation, or starts a new one.
    A contact could have multiple closed conversations over time (e.g. one
    per past inquiry) but only ever one open thread at a time.
    """
    conversation = (
        db.query(Conversation)
        .filter(Conversation.contact_id == contact.id, Conversation.status == "open")
        .first()
    )
    if conversation:
        return conversation

    conversation = Conversation(contact_id=contact.id, status="open")
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation


def get_conversation(db: Session, conversation_id) -> Optional[Conversation]:
    return db.query(Conversation).filter(Conversation.id == conversation_id).first()


def list_conversations_with_previews(db: Session) -> list[dict]:
    """
    Returns conversations newest-first, each paired with its contact and
    latest message. Implemented as a straightforward N+1 query for now -
    fine at this stage; the first real target for query optimization
    (a single joined/windowed query) once conversation volume matters.
    """
    conversations = (
        db.query(Conversation)
        .join(Contact)
        .order_by(Conversation.updated_at.desc())
        .all()
    )

    results = []
    for conversation in conversations:
        last_message = (
            db.query(Message)
            .filter(Message.conversation_id == conversation.id)
            .order_by(Message.created_at.desc())
            .first()
        )
        results.append({"conversation": conversation, "last_message": last_message})

    return results


def list_messages(db: Session, conversation_id) -> list[Message]:
    return (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
        .all()
    )
