"""Company profile endpoints - a singleton resource, not a list."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import require_admin
from app.db.session import get_db
from app.schemas.company import CompanyRead, CompanyUpdate
from app.services import company_service

router = APIRouter(prefix="/company", tags=["company"], dependencies=[Depends(require_admin)])


@router.get("", response_model=CompanyRead)
def get_company(db: Session = Depends(get_db)):
    return company_service.get_company_read(db)


@router.put("", response_model=CompanyRead)
def update_company(payload: CompanyUpdate, db: Session = Depends(get_db)):
    return company_service.update_company(db, payload)
