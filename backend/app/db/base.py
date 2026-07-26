"""
SQLAlchemy declarative base.

Every ORM model in app/models/ inherits from this Base. Kept in its own
module (rather than in session.py) so Alembic's env.py can import model
metadata without also importing the engine/session machinery.
"""
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
