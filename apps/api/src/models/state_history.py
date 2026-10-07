from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from sqlalchemy import (
    DateTime,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class StateSnapshot(Base):
    """
    Immutable canonical-state snapshot.

    Redis = latest state.
    PostgreSQL = historical state snapshots.
    """

    __tablename__ = "state_snapshots"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    entity_type: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
    )

    chain: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
    )

    entity_id: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    version: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
    )

    source_id: Mapped[str | None] = mapped_column(
        String(128),
        nullable=True,
    )

    event_id: Mapped[str | None] = mapped_column(
        String(128),
        nullable=True,
    )

    observed_at: Mapped[
        datetime | None
    ] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    processed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )

    payload: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
    )

    __table_args__ = (
        Index(
            "ix_state_snapshots_entity",
            "entity_type",
            "chain",
            "entity_id",
            "version",
        ),
        Index(
            "ix_state_snapshots_processed",
            "processed_at",
        ),
    )