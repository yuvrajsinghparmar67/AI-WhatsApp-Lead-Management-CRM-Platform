"""
Ensures app.core.config.Settings can be instantiated during tests without
requiring a real .env file - SECRET_KEY and DATABASE_URL are required
fields with no default. These are dummy values; nothing in the unit test
suite actually connects to a database.
"""
import os

os.environ.setdefault("SECRET_KEY", "test-secret-key-not-for-production")
os.environ.setdefault("DATABASE_URL", "postgresql+psycopg2://test:test@localhost:5432/test")
