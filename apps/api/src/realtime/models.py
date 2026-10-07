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
    "chain.observed",
]


EventStatus = Literal[
    "observed",
    "derived",
    "model_derived",
    "unresolved",
    "conflict",
    
    # Intelligence events
    "rug.updated",
    "market_intelligence.updated",
    "wallet_dna.updated",
    "j7.updated",
    "narrative.updated",

    # Scoring / alerts
    "score.updated",
    "alert.created",

    # System
    "system.updated",
]


class ChainPosition(BaseModel):
    """
    Blockchain position associated with an observed event.

    Depending on chain:
    - Solana: slot
    - EVM: block_number
    """

    block_number: int | None = None
    block_hash: str | None = None

    slot: int | None = None

    transaction_hash: str | None = None
    transaction_signature: str | None = None

    instruction_index: int | None = None
    log_index: int | None = None

    commitment: str | None = None


class EventEvidence(BaseModel):
    """
    Evidence supporting an event or attribution.
    """

    type: str
    value: str
    source: str | None = None


class RealtimeEvent(BaseModel):
    """
    Canonical SentinelAI realtime event.

    Facts should be observed directly.
    Derived/model-generated values must identify themselves
    through `status` and provenance.
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
        default_factory=lambda: datetime.now(
            timezone.utc
        )
    )

    processed_at: datetime | None = None

    chain_position: ChainPosition | None = None

    evidence: list[EventEvidence] = Field(
        default_factory=list
    )

    parser_name: str | None = None
    parser_version: str | None = None

    model_name: str | None = None
    model_version: str | None = None

    parent_event_ids: list[str] = Field(
        default_factory=list
    )

    status: EventStatus = "observed"

    version: int = 1

    def with_processed_timestamp(
        self,
    ) -> "RealtimeEvent":
        return self.model_copy(
            update={
                "processed_at": datetime.now(
                    timezone.utc
                )
            }
        )

    def age_ms(self) -> float:
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
        data = self.model_dump(
            mode="json"
        )

        data["age_ms"] = round(
            self.age_ms(),
            2,
        )

        return data