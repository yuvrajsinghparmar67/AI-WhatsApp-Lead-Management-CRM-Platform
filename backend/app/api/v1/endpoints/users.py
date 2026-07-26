"""Team member management endpoints - admin-only."""
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import require_admin
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserRead, UserUpdate
from app.services import user_service

router = APIRouter(prefix="/users", tags=["users"], dependencies=[Depends(require_admin)])


@router.get("", response_model=list[UserRead])
def list_users(db: Session = Depends(get_db)):
    return user_service.list_users(db)


@router.patch("/{user_id}", response_model=UserRead)
def update_user(
    user_id: uuid.UUID,
    payload: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    target_user = user_service.get_user(db, user_id)
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        return user_service.update_user(db, target_user, current_user, payload.role, payload.is_active)
    except user_service.SelfModificationError as e:
        raise HTTPException(status_code=400, detail=str(e))
