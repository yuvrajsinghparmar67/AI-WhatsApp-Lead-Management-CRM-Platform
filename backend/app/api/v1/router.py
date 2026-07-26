"""
Aggregates every endpoint module under app/api/v1/endpoints/ into one
router that main.py mounts under settings.API_V1_PREFIX. Adding a new
resource means adding a new endpoints/<resource>.py file and one
include_router() line here.
"""
from fastapi import APIRouter

from app.api.v1.endpoints import (
    ai_settings,
    analytics,
    auth,
    business_rules,
    catalog,
    company,
    contacts,
    conversations,
    faq,
    follow_up_rules,
    health,
    knowledge_base,
    prompt_settings,
    simulator,
    users,
)

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(contacts.router)
api_router.include_router(conversations.router)
api_router.include_router(simulator.router)
api_router.include_router(analytics.router)
api_router.include_router(company.router)
api_router.include_router(knowledge_base.router)
api_router.include_router(catalog.router)
api_router.include_router(faq.router)
api_router.include_router(business_rules.router)
api_router.include_router(follow_up_rules.router)
api_router.include_router(ai_settings.router)
api_router.include_router(prompt_settings.router)
api_router.include_router(users.router)
