from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import (
    BigInteger,
    DateTime,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class CanonicalStateRevision(Base):
    """
    Append-only durable state revision.

    Redis = latest state.
    PostgreSQL = durable state history / recovery source.
    """

    __tablename__ = "canonical_state_revisions"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    entity_type: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
    )

    entity_id: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    chain: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
    )

    version: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    state_status: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
    )

    observed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    event_id: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    source: Mapped[str | None] = mapped_column(
        String(128),
        nullable=True,
    )

    source_type: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True,
    )

    payload: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
    )

    __table_args__ = (
        Index(
            "ix_state_revision_entity",
            "entity_type",
            "entity_id",
            "chain",
        ),
        Index(
            "ix_state_revision_version",
            "entity_type",
            "entity_id",
            "version",
        ),
        Index(
            "ix_state_revision_observed_at",
            "observed_at",
        ),
        Index(
            "ix_state_revision_event_id",
            "event_id",
        ),
    )