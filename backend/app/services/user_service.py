"""
Business logic for team member management. Admin-only (enforced at the
route layer via app/api/deps.py::require_admin) - this module itself
enforces the one CRM-specific safety rule: an admin can't lock themselves
out by demoting or deactivating their own account.
"""
from app.models.user import User


class SelfModificationError(ValueError):
    """Raised when an admin tries to demote/deactivate their own account."""


def list_users(db) -> list[User]:
    return db.query(User).order_by(User.created_at.asc()).all()


def get_user(db, user_id) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def update_user(db, target_user: User, current_user: User, role: str | None, is_active: bool | None) -> User:
    if target_user.id == current_user.id:
        if role is not None and role != "admin":
            raise SelfModificationError("You can't remove your own admin role.")
        if is_active is False:
            raise SelfModificationError("You can't deactivate your own account.")

    if role is not None:
        target_user.role = role
    if is_active is not None:
        target_user.is_active = is_active

    db.commit()
    db.refresh(target_user)
    return target_user
