"""Unit tests for the team-management self-modification guard."""
import uuid

import pytest

from app.models.user import User
from app.services.user_service import SelfModificationError, update_user


class _FakeDB:
    """Stands in for a SQLAlchemy Session - just needs commit/refresh to be no-ops."""

    def commit(self):
        pass

    def refresh(self, obj):
        pass


def _make_user(role="agent", is_active=True):
    return User(id=uuid.uuid4(), email="a@example.com", full_name="A", hashed_password="x", role=role, is_active=is_active)


def test_admin_can_change_someone_elses_role():
    admin = _make_user(role="admin")
    other = _make_user(role="agent")

    updated = update_user(_FakeDB(), other, admin, role="admin", is_active=None)

    assert updated.role == "admin"


def test_admin_cannot_demote_themselves():
    admin = _make_user(role="admin")

    with pytest.raises(SelfModificationError):
        update_user(_FakeDB(), admin, admin, role="agent", is_active=None)


def test_admin_cannot_deactivate_themselves():
    admin = _make_user(role="admin")

    with pytest.raises(SelfModificationError):
        update_user(_FakeDB(), admin, admin, role=None, is_active=False)


def test_admin_can_activate_themselves_noop():
    """Setting is_active=True on yourself is allowed - it's only turning yourself off that's blocked."""
    admin = _make_user(role="admin")

    updated = update_user(_FakeDB(), admin, admin, role=None, is_active=True)

    assert updated.is_active is True
