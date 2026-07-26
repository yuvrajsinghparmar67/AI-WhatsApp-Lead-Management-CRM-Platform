"""
Business logic for Contacts.

Kept separate from api/ so that any future caller (a real webhook handler,
a background job, a script) can reuse the same "find or create a contact"
logic instead of duplicating it inside a route function.
"""
import csv
import io
from typing import Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.contact import Contact


def get_or_create_contact(db: Session, phone_number: str, display_name: Optional[str] = None) -> Contact:
    contact = db.query(Contact).filter(Contact.phone_number == phone_number).first()
    if contact:
        # Backfill the display name if we learn it later and didn't have one
        if display_name and not contact.display_name:
            contact.display_name = display_name
            db.commit()
            db.refresh(contact)
        return contact

    contact = Contact(phone_number=phone_number, display_name=display_name)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


def list_contacts(
    db: Session,
    search: Optional[str] = None,
    lead_status: Optional[str] = None,
    priority: Optional[str] = None,
    sentiment: Optional[str] = None,
) -> list[Contact]:
    """
    Powers both the Customer Database screen and CSV export - the same
    filters apply to each, so what an agent sees on screen is exactly
    what they get in the download (Milestone 16).
    """
    query = db.query(Contact)

    if search:
        needle = f"%{search.strip()}%"
        query = query.filter(or_(Contact.display_name.ilike(needle), Contact.phone_number.ilike(needle)))
    if lead_status:
        query = query.filter(Contact.lead_status == lead_status)
    if priority:
        query = query.filter(Contact.priority == priority)
    if sentiment:
        query = query.filter(Contact.sentiment == sentiment)

    return query.order_by(Contact.updated_at.desc()).all()


def get_contact(db: Session, contact_id) -> Optional[Contact]:
    return db.query(Contact).filter(Contact.id == contact_id).first()


def update_contact(db: Session, contact: Contact, lead_status: Optional[str] = None, priority: Optional[str] = None) -> Contact:
    """
    Manual override for AI-derived fields - e.g. an agent drags a card to a
    different pipeline column, or corrects a priority the AI got wrong.
    Only touches fields that were actually provided.
    """
    if lead_status is not None:
        contact.lead_status = lead_status
    if priority is not None:
        contact.priority = priority

    db.commit()
    db.refresh(contact)
    return contact


_CSV_HEADERS = [
    "Name", "Phone Number", "Lead Status", "Priority",
    "Sentiment", "Estimated Budget", "Confidence Score", "Created At", "Updated At",
]


def contacts_to_csv(contacts: list[Contact]) -> str:
    """Renders a contact list to CSV text for the Customer Database export."""
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(_CSV_HEADERS)
    for contact in contacts:
        writer.writerow([
            contact.display_name or "",
            contact.phone_number,
            contact.lead_status,
            contact.priority,
            contact.sentiment or "",
            contact.estimated_budget if contact.estimated_budget is not None else "",
            contact.confidence_score if contact.confidence_score is not None else "",
            contact.created_at.isoformat() if contact.created_at else "",
            contact.updated_at.isoformat() if contact.updated_at else "",
        ])
    return buffer.getvalue()
