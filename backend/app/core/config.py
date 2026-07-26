"""
Central application configuration.

Every configurable value in the app (secrets, DB URL, AI provider choice,
messaging provider choice, CORS origins, etc.) is read from environment
variables through this single Settings object. Nothing else in the codebase
should call os.environ directly - this keeps configuration centralized,
type-validated, and easy to override per environment (dev / staging / prod).
"""
from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # --- App ---
    APP_NAME: str = "AI WhatsApp CRM"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"

    # --- Security ---
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # --- Database ---
    DATABASE_URL: str

    # --- AI Provider ---
    AI_PROVIDER: str = "gemini"
    GEMINI_API_KEY: str = ""
    GEMINI_CHAT_MODEL: str = "gemini-3.5-flash"
    GEMINI_EMBEDDING_MODEL: str = "gemini-embedding-2"

    # --- Messaging Provider ---
    MESSAGING_PROVIDER: str = "simulated"

    # --- Follow-up Rules scheduler ---
    FOLLOW_UP_SCHEDULER_ENABLED: bool = True
    FOLLOW_UP_SCHEDULER_INTERVAL_MINUTES: int = 15

    # --- CORS ---
    CORS_ORIGINS: str = "http://localhost:5173"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]


@lru_cache
def get_settings() -> "Settings":
    """
    Cached settings accessor.

    Using lru_cache means the .env file is parsed once per process instead
    of on every request - FastAPI's Depends(get_settings) can be used
    anywhere a route/service needs config without a performance cost.
    """
    return Settings()


settings = get_settings()
