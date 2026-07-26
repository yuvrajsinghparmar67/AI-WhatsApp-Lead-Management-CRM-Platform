"""
Unit tests for the Follow-up Rules matching/rendering logic. These stay
DB-free by testing rule_matches_conversation() and render_message()
directly with plain model instances - the same pattern
test_user_service.py uses for update_user()'s self-modification guard.
The DB-touching orchestration (run_due_follow_ups) is exercised manually
via the "Run now" button per the milestone's testing steps, same as the
rest of this project's service layer.
"""
import uuid

from app.models.contact import Contact
from app.models.follow_up_rule import FollowUpRule
from app.services.follow_up_rule_service import render_message, rule_matches_conversation


def _make_rule(idle_hours=24, lead_status_filter=None, is_active=True, message_template="Hi {display_name}, still there?"):
    return FollowUpRule(
        id=uuid.uuid4(),
        name="Test rule",
        is_active=is_active,
        idle_hours=idle_hours,
        lead_status_filter=lead_status_filter,
        message_template=message_template,
    )


def test_matches_when_idle_long_enough_and_inbound():
    rule = _make_rule(idle_hours=24)
    assert rule_matches_conversation(
        rule, contact_lead_status="new", last_message_direction="inbound", hours_since_last_message=25
    )


def test_does_not_match_before_idle_threshold():
    rule = _make_rule(idle_hours=24)
    assert not rule_matches_conversation(
        rule, contact_lead_status="new", last_message_direction="inbound", hours_since_last_message=5
    )


def test_does_not_match_when_last_message_is_outbound():
    """An agent, AI, or prior follow-up reply resets the clock."""
    rule = _make_rule(idle_hours=24)
    assert not rule_matches_conversation(
        rule, contact_lead_status="new", last_message_direction="outbound", hours_since_last_message=48
    )


def test_does_not_match_inactive_rule():
    rule = _make_rule(idle_hours=24, is_active=False)
    assert not rule_matches_conversation(
        rule, contact_lead_status="new", last_message_direction="inbound", hours_since_last_message=48
    )


def test_does_not_match_won_or_lost_contacts():
    rule = _make_rule(idle_hours=24)
    for status in ("won", "lost"):
        assert not rule_matches_conversation(
            rule, contact_lead_status=status, last_message_direction="inbound", hours_since_last_message=48
        )


def test_lead_status_filter_excludes_non_matching_contacts():
    rule = _make_rule(idle_hours=24, lead_status_filter="qualified")
    assert not rule_matches_conversation(
        rule, contact_lead_status="new", last_message_direction="inbound", hours_since_last_message=48
    )
    assert rule_matches_conversation(
        rule, contact_lead_status="qualified", last_message_direction="inbound", hours_since_last_message=48
    )


def test_no_lead_status_filter_matches_any_open_status():
    rule = _make_rule(idle_hours=24, lead_status_filter=None)
    for status in ("new", "qualified", "nurturing"):
        assert rule_matches_conversation(
            rule, contact_lead_status=status, last_message_direction="inbound", hours_since_last_message=48
        )


def test_render_message_fills_in_display_name():
    rule = _make_rule(message_template="Hi {display_name}, just checking in!")
    contact = Contact(id=uuid.uuid4(), phone_number="+15550001111", display_name="Priya")
    assert render_message(rule, contact) == "Hi Priya, just checking in!"


def test_render_message_falls_back_when_no_display_name():
    rule = _make_rule(message_template="Hi {display_name}, just checking in!")
    contact = Contact(id=uuid.uuid4(), phone_number="+15550001111", display_name=None)
    assert render_message(rule, contact) == "Hi there, just checking in!"


def test_render_message_falls_back_on_malformed_template():
    """An unknown placeholder shouldn't crash the scheduler - just send the raw text."""
    rule = _make_rule(message_template="Hi {nonexistent_field}!")
    contact = Contact(id=uuid.uuid4(), phone_number="+15550001111", display_name="Priya")
    assert render_message(rule, contact) == "Hi {nonexistent_field}!"
