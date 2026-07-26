"""
Unit tests for contact_service.contacts_to_csv() - the Customer Database
export (Milestone 16). Stays DB-free by building Contact instances
directly and checking the rendered CSV text, the same pattern
test_follow_up_rules.py uses for its pure functions. The filtering logic
in list_contacts() builds a real SQLAlchemy query and is exercised via
this milestone's manual testing steps instead, same as the rest of this
project's DB-touching service code.
"""
import csv
import io
import uuid
from datetime import datetime, timezone

from app.models.contact import Contact
from app.services.contact_service import contacts_to_csv


def _make_contact(**overrides):
    defaults = dict(
        id=uuid.uuid4(),
        phone_number="+15550001111",
        display_name="Priya Shah",
        lead_status="qualified",
        priority="high",
        sentiment="positive",
        estimated_budget=5000.0,
        confidence_score=0.82,
        created_at=datetime(2026, 7, 1, tzinfo=timezone.utc),
        updated_at=datetime(2026, 7, 2, tzinfo=timezone.utc),
    )
    defaults.update(overrides)
    return Contact(**defaults)


def test_csv_includes_header_row():
    rows = list(csv.reader(io.StringIO(contacts_to_csv([]))))
    assert rows == [[
        "Name", "Phone Number", "Lead Status", "Priority",
        "Sentiment", "Estimated Budget", "Confidence Score", "Created At", "Updated At",
    ]]


def test_csv_renders_a_contact_row():
    rows = list(csv.reader(io.StringIO(contacts_to_csv([_make_contact()]))))
    assert rows[1][:5] == ["Priya Shah", "+15550001111", "qualified", "high", "positive"]


def test_csv_handles_missing_optional_fields():
    contact = _make_contact(display_name=None, sentiment=None, estimated_budget=None, confidence_score=None)
    rows = list(csv.reader(io.StringIO(contacts_to_csv([contact]))))
    name, phone, lead_status, priority, sentiment, budget, confidence, *_ = rows[1]
    assert name == ""
    assert sentiment == ""
    assert budget == ""
    assert confidence == ""


def test_csv_renders_one_row_per_contact_in_order():
    contacts = [_make_contact(display_name="First"), _make_contact(display_name="Second")]
    rows = list(csv.reader(io.StringIO(contacts_to_csv(contacts))))
    assert [row[0] for row in rows[1:]] == ["First", "Second"]
