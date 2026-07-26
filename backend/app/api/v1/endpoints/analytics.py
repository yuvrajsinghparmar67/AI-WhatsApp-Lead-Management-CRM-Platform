"""Analytics endpoint - a single aggregate payload powering the dashboard."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.schemas.analytics import AnalyticsOverview
from app.services import analytics_service

router = APIRouter(prefix="/analytics", tags=["analytics"], dependencies=[Depends(get_current_user)])


@router.get("/overview", response_model=AnalyticsOverview)
def get_overview(db: Session = Depends(get_db)):
    return analytics_service.get_overview(db)
