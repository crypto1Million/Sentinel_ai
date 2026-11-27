from __future__ import annotations

from sqlalchemy.orm import sessionmaker

from database.connection import engine


SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()