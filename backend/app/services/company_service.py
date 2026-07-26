"""
Business logic for the singleton Company profile.

business_hours is stored on the model as a JSON string (see
app/models/company.py); this service is the only place that
serializes/deserializes it, so callers (the API layer, the AI pipeline)
always work with a plain list of BusinessHoursDay, never raw JSON text.
"""
import json
import uuid

from sqlalchemy.orm import Session

from app.models.company import Company
from app.schemas.company import BusinessHoursDay, CompanyRead, CompanyUpdate

DEFAULT_BUSINESS_HOURS = [
    BusinessHoursDay(day=day, closed=False, open="09:00", close="18:00")
    for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
] + [
    BusinessHoursDay(day=day, closed=True) for day in ["Saturday", "Sunday"]
]


def _parse_hours(raw: str | None) -> list[BusinessHoursDay]:
    if not raw:
        return DEFAULT_BUSINESS_HOURS
    try:
        return [BusinessHoursDay.model_validate(day) for day in json.loads(raw)]
    except Exception:
        return DEFAULT_BUSINESS_HOURS


def _to_read_schema(company: Company) -> CompanyRead:
    return CompanyRead(
        id=company.id,
        business_name=company.business_name,
        address=company.address,
        phone=company.phone,
        email=company.email,
        website=company.website,
        business_hours=_parse_hours(company.business_hours),
        updated_at=company.updated_at,
    )


def get_or_create_company(db: Session) -> Company:
    """The app treats this as a singleton - there's ever only one row."""
    company = db.query(Company).first()
    if company:
        return company

    company = Company(id=uuid.uuid4())
    db.add(company)
    db.commit()
    db.refresh(company)
    return company


def get_company_read(db: Session) -> CompanyRead:
    return _to_read_schema(get_or_create_company(db))


def update_company(db: Session, updates: CompanyUpdate) -> CompanyRead:
    company = get_or_create_company(db)

    if updates.business_name is not None:
        company.business_name = updates.business_name
    if updates.address is not None:
        company.address = updates.address
    if updates.phone is not None:
        company.phone = updates.phone
    if updates.email is not None:
        company.email = updates.email
    if updates.website is not None:
        company.website = updates.website
    if updates.business_hours is not None:
        company.business_hours = json.dumps([day.model_dump() for day in updates.business_hours])

    db.commit()
    db.refresh(company)
    return _to_read_schema(company)


def format_company_profile_for_ai(db: Session) -> str | None:
    """
    Formats the company profile as short, readable text for the AI
    prompt - e.g. "Business: Iron Peak Gym | Phone: +1 555 0100 | Hours:
    Mon-Fri 9:00-18:00, Sat-Sun Closed". Returns None if nothing has been
    filled in yet, so the prompt doesn't inject an empty/useless block.
    """
    company = get_company_read(db)

    parts = []
    if company.business_name:
        parts.append(f"Business name: {company.business_name}")
    if company.address:
        parts.append(f"Address: {company.address}")
    if company.phone:
        parts.append(f"Phone: {company.phone}")
    if company.email:
        parts.append(f"Email: {company.email}")
    if company.website:
        parts.append(f"Website: {company.website}")

    hours_lines = [
        f"{d.day}: {'Closed' if d.closed else f'{d.open}-{d.close}'}" for d in company.business_hours
    ]
    if any(not d.closed for d in company.business_hours):
        parts.append("Business hours: " + "; ".join(hours_lines))

    if not parts:
        return None
    return "\n".join(parts)
