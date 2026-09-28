from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, Field


EventType = Literal[
    "token.updated",
    "wallet.updated",
    "score.updated",
    "alert.created",
    "pool.updated",
    "launchpad.detected",
    "system.updated",
]


class RealtimeEvent(BaseModel):
    """
    Canonical realtime event exchanged between SentinelAI
    backend services and the websocket layer.

    This object contains metadata about where the event came from.
    It does not invent domain values.
    """

    event_id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    event_type: EventType

    entity_type: str
    entity_id: str

    chain: str | None = None

    payload: dict[str, Any] = Field(
        default_factory=dict
    )

    source: str
    source_id: str | None = None

    observed_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    processed_at: datetime | None = None

    status: Literal[
        "observed",
        "derived",
        "model_derived",
        "unresolved",
        "conflict",
    ] = "observed"

    version: int = 1

    def with_processed_timestamp(
        self,
    ) -> "RealtimeEvent":
        """
        Return a copy containing the backend processing timestamp.
        """
        return self.model_copy(
            update={
                "processed_at": datetime.now(
                    timezone.utc
                )
            }
        )

    def age_ms(self) -> float:
        """
        Age of the observed event relative to now.
        """
        now = datetime.now(timezone.utc)

        observed = self.observed_at

        if observed.tzinfo is None:
            observed = observed.replace(
                tzinfo=timezone.utc
            )

        return max(
            0.0,
            (
                now - observed
            ).total_seconds()
            * 1000,
        )

    def to_wire(self) -> dict[str, Any]:
        """
        Wire representation sent over websocket.
        """
        event = self.model_dump(
            mode="json"
        )

        event["age_ms"] = round(
            self.age_ms(),
            2,
        )

        return event