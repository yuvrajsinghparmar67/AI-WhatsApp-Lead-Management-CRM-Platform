"""
Authentication endpoints: register + login.

This is intentionally minimal in Milestone 1 (just enough to prove the
auth mechanics work end-to-end). Full account management, password reset,
etc. land in a later milestone alongside the rest of the CRM.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.security import create_access_token, hash_password, verify_password
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, Token
from app.schemas.user import UserCreate, UserRead

router = APIRouter()


@router.post("/auth/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)) -> User:
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # The very first account ever created becomes admin (bootstraps the
    # Admin Portal without a separate seeding step); every account after
    # that defaults to "agent" per the User model's column default. There's
    # no invite-only signup yet - see the README's known limitations.
    is_first_user = db.query(User).count() == 0

    user = User(
        email=payload.email,
        full_name=payload.full_name,
        hashed_password=hash_password(payload.password),
        role="admin" if is_first_user else "agent",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/auth/login", response_model=Token)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> Token:
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    access_token = create_access_token(subject=user.email)
    return Token(access_token=access_token)


@router.get("/auth/me", response_model=UserRead)
def get_me(current_user: User = Depends(get_current_user)) -> User:
    """Resolves the logged-in user from their JWT - used by the frontend on load to restore a session."""
    return current_user
