"""Contact endpoints - read/search the lead list, export it, and manually override AI-derived fields."""
import uuid
from datetime import datetime, timezone
from typing import Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.schemas.contact import ContactRead, ContactUpdate
from app.services import contact_service

router = APIRouter(prefix="/contacts", tags=["contacts"], dependencies=[Depends(get_current_user)])


@router.get("", response_model=list[ContactRead])
def list_contacts(
    search: Optional[str] = Query(None, description="Matches against name or phone number"),
    lead_status: Optional[Literal["new", "qualified", "nurturing", "won", "lost"]] = None,
    priority: Optional[Literal["low", "medium", "high", "urgent"]] = None,
    sentiment: Optional[Literal["positive", "neutral", "negative"]] = None,
    db: Session = Depends(get_db),
):
    return contact_service.list_contacts(db, search=search, lead_status=lead_status, priority=priority, sentiment=sentiment)


@router.get("/export")
def export_contacts(
    search: Optional[str] = None,
    lead_status: Optional[Literal["new", "qualified", "nurturing", "won", "lost"]] = None,
    priority: Optional[Literal["low", "medium", "high", "urgent"]] = None,
    sentiment: Optional[Literal["positive", "neutral", "negative"]] = None,
    db: Session = Depends(get_db),
):
    """
    CSV download of the customer database. Takes the same search/filter
    params as the list endpoint, so exporting always matches whatever's
    currently shown on screen (Milestone 16). Registered ahead of
    `/{contact_id}` below - otherwise "export" would be parsed as a UUID
    and 422 instead of matching this route.
    """
    contacts = contact_service.list_contacts(db, search=search, lead_status=lead_status, priority=priority, sentiment=sentiment)
    csv_body = contact_service.contacts_to_csv(contacts)
    filename = f"contacts-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}.csv"
    return StreamingResponse(
        iter([csv_body]),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.get("/{contact_id}", response_model=ContactRead)
def get_contact(contact_id: uuid.UUID, db: Session = Depends(get_db)):
    contact = contact_service.get_contact(db, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.patch("/{contact_id}", response_model=ContactRead)
def update_contact(contact_id: uuid.UUID, payload: ContactUpdate, db: Session = Depends(get_db)):
    """Manual override - e.g. dragging a card to a new pipeline column."""
    contact = contact_service.get_contact(db, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    return contact_service.update_contact(db, contact, lead_status=payload.lead_status, priority=payload.priority)
