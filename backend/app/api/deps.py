"""
Shared FastAPI dependencies (DB session, current-user resolution from JWT).
Import these in route files instead of re-implementing auth checks per route.
"""
from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    email = decode_access_token(token)
    if email is None:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception

    return user


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """
    Gate for the Admin Portal (business info, catalog, FAQs, knowledge
    base, business rules, AI/prompt settings, team management). Agents
    can log in and use the Inbox/Contacts/Analytics - the normal CRM
    workflow - but nothing under this gate. Raises 403 (not 401 - the
    user IS authenticated, they just aren't allowed here) so the frontend
    can tell "not logged in" apart from "logged in but not permitted".
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This action requires an admin account.",
        )
    return current_user
