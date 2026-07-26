"""
Application entrypoint. Creates the FastAPI app, wires up middleware,
configures logging, and mounts the versioned API router.

Run with: uvicorn app.main:app --reload
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.logging import configure_logging
from app.scheduler.setup import start_scheduler, stop_scheduler

configure_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Starts the Follow-up Rules scheduler (Milestone 15) alongside the API
    # server, and shuts it down cleanly on process exit.
    start_scheduler()
    yield
    stop_scheduler()


app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    description="AI-powered WhatsApp Lead Management & CRM Platform - API",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/", tags=["root"])
async def root() -> dict:
    return {"message": f"{settings.APP_NAME} API", "docs": "/docs"}
