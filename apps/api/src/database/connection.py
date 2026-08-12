from sqlalchemy import create_engine

from config.settings import get_settings


settings = get_settings()

DATABASE_URL = (

    f"postgresql+psycopg2://"

    f"{settings.POSTGRES_USER}:"

    f"{settings.POSTGRES_PASSWORD}@"

    f"postgres:5432/"

    f"{settings.POSTGRES_DB}"
)

engine = create_engine(

    DATABASE_URL,

    pool_pre_ping=True,

    pool_size=20,

    max_overflow=30
)