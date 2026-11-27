from database.connection import engine

from models.base import Base

# Register canonical state models.
from database.canonical_state import (  # noqa: F401
    CanonicalStateRevision,
)


def init_database() -> None:
    Base.metadata.create_all(
        bind=engine
    )

    print(
        "Database initialized."
    )