from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.engine import URL

from config.settings import get_settings


settings = get_settings()


def build_database_url() -> URL:
    host = settings.POSTGRES_HOST
    port = settings.POSTGRES_PORT
    user = settings.POSTGRES_USER
    password = settings.POSTGRES_PASSWORD
    database = settings.POSTGRES_DB

    if not host:
        raise RuntimeError(
            "POSTGRES_HOST is not configured"
        )

    if not user:
        raise RuntimeError(
            "POSTGRES_USER is not configured"
        )

    if not password:
        raise RuntimeError(
            "POSTGRES_PASSWORD is not configured"
        )

    if not database:
        raise RuntimeError(
            "POSTGRES_DB is not configured"
        )

    return URL.create(
        drivername="postgresql+psycopg",
        username=user,
        password=password,
        host=host,
        port=port,
        database=database,
    )


DATABASE_URL = build_database_url()


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=20,
    max_overflow=30,
    pool_recycle=1800,
)