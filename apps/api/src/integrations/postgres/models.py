"""
Base PostgreSQL Models
======================
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    DateTime,
    Integer,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)


###############################################################################
# Base
###############################################################################


class Base(DeclarativeBase):
    """
    SQLAlchemy Declarative Base.
    """

    pass


###############################################################################
# Timestamp Mixin
###############################################################################


class TimestampMixin:

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )


###############################################################################
# ID Mixin
###############################################################################


class IDMixin:

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )


###############################################################################
# Runtime
###############################################################################


def summary():

    return {
        "base": "SQLAlchemy Declarative",
        "mixins": [
            "IDMixin",
            "TimestampMixin",
        ],
    }


###############################################################################
# Utilities
###############################################################################


def metadata():

    return Base.metadata