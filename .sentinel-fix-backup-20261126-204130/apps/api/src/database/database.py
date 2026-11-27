from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.settings import settings
# Backwards-compatible aliases.
# The engine is defined only in connection.py.

from database.connection import engine
from database.session import SessionLocal

__all__ = [
    "engine",
    "SessionLocal",
]

engine = create_engine(
    settings.DATABASE_URL
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)