from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator


class EventStatus(str, Enum):
    RECEIVED = "received"
    VALIDATED = "validated"
    PROCESSED = "processed"
    REJECTED = "rejected"
    REPLAYED = "replayed"


class DataQuality(str, Enum):
    VERIFIED = "verified"
    DERIVED = "derived"
    MODEL_DERIVED = "model_derived"
    STALE = "stale"
    CONFLICT = "conflict"
    UNRESOLVED = "unresolved"
    UNAVAILABLE = "unavailable"


class CommitmentLevel(str, Enum):
    PROCESSED = "processed"
    CONFIRMED = "confirmed"
    FINALIZED = "finalized"


class SourceTransport(str, Enum):
    WEBSOCKET = "websocket"
    RPC = "rpc"
    HTTP = "http"
    WEBHOOK = "webhook"
    STREAM = "stream"
    REPLAY = "replay"


class SourceMetadata(BaseModel):
    """
    Describes where the observation came from.

    This is intentionally independent of the provider implementation so
    Helius, Alchemy, direct RPC, protocol APIs, etc. can all use the same
    canonical structure.
    """

    model_config = ConfigDict(extra="forbid")

    provider: str
    transport: SourceTransport
    source_id: str | None = None

    endpoint: str | None = None

    provider_event_id: str | None = None
    provider_cursor: str | None = None

    observed_at: datetime | None = None


class ChainPosition(BaseModel):
    """
    Chain-native location of an event.

    Solana:
        slot + transaction_signature + instruction_index

    EVM:
        block_number + block_hash + transaction_hash + log_index
    """

    model_config = ConfigDict(extra="forbid")

    slot: int | None = Field(default=None, ge=0)

    block_number: int | None = Field(default=None, ge=0)
    block_hash: str | None = None

    transaction_signature: str | None = None
    transaction_hash: str | None = None

    instruction_index: int | None = Field(default=None, ge=0)
    log_index: int | None = Field(default=None, ge=0)

    commitment: CommitmentLevel | None = None


class Evidence(BaseModel):
    """
    Atomic evidence attached to an event.

    Example:
        type = "program_id"
        value = "LanMV9..."
    """

    model_config = ConfigDict(extra="forbid")

    type: str
    value: str

    description: str | None = None

    source: str | None = None
    verified: bool = True


class ParserMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    version: str

    schema_version: str = "1.0"

    deterministic: bool = True


class EventEnvelope(BaseModel):
    """
    Canonical SentinelAI event contract.

    Every external observation MUST become an EventEnvelope before it
    reaches:
        - state reducers
        - scoring
        - Rug Radar
        - Wallet DNA
        - J7Tracker
        - alerts
        - persistence
        - websocket delivery
        - replay
    """

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        use_enum_values=True,
    )

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    event_id: str = Field(default_factory=lambda: str(uuid4()))
    event_type: str

    schema_version: str = "1.0"

    # ---------------------------------------------------------
    # Entity
    # ---------------------------------------------------------

    chain: str
    entity_type: str
    entity_id: str

    # Optional secondary entity.
    # Useful for:
    # token <-> pool
    # wallet <-> token
    # token <-> launchpad
    related_entity_type: str | None = None
    related_entity_id: str | None = None

    # ---------------------------------------------------------
    # Timing
    # ---------------------------------------------------------

    observed_at: datetime
    received_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    processed_at: datetime | None = None

    # ---------------------------------------------------------
    # Ordering / correlation
    # ---------------------------------------------------------

    sequence: int | None = Field(default=None, ge=0)

    correlation_id: str | None = None
    parent_event_ids: list[str] = Field(default_factory=list)

    # ---------------------------------------------------------
    # Chain information
    # ---------------------------------------------------------

    chain_position: ChainPosition | None = None

    # ---------------------------------------------------------
    # Provenance
    # ---------------------------------------------------------

    source: SourceMetadata
    parser: ParserMetadata

    # ---------------------------------------------------------
    # Evidence
    # ---------------------------------------------------------

    evidence: list[Evidence] = Field(default_factory=list)

    # ---------------------------------------------------------
    # Quality
    # ---------------------------------------------------------

    status: EventStatus = EventStatus.RECEIVED
    quality: DataQuality = DataQuality.VERIFIED

    # ---------------------------------------------------------
    # Payload
    # ---------------------------------------------------------

    payload: dict[str, Any]

    # ---------------------------------------------------------
    # Provider/raw data
    # ---------------------------------------------------------

    raw_payload: dict[str, Any] | None = None

    # ---------------------------------------------------------
    # Additional metadata
    # ---------------------------------------------------------

    metadata: dict[str, Any] = Field(default_factory=dict)

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    @field_validator("observed_at", "received_at", "processed_at")
    @classmethod
    def ensure_utc(
        cls,
        value: datetime | None,
    ) -> datetime | None:
        if value is None:
            return None

        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)

        return value.astimezone(timezone.utc)

    @field_validator("entity_id", "chain", "entity_type")
    @classmethod
    def validate_identity_fields(
        cls,
        value: str,
    ) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Identity fields cannot be empty.")

        return value

    # ---------------------------------------------------------
    # Derived properties
    # ---------------------------------------------------------

    @property
    def observation_age_ms(self) -> int:
        """
        Approximate age between observation and processing time.

        If processing hasn't happened yet, compare against current time.
        """

        end = self.processed_at or datetime.now(timezone.utc)

        delta = end - self.observed_at
        return max(0, int(delta.total_seconds() * 1000))

    @property
    def processing_latency_ms(self) -> int | None:
        """
        Time between receiving and processing the event.
        """

        if self.processed_at is None:
            return None

        delta = self.processed_at - self.received_at
        return max(0, int(delta.total_seconds() * 1000))

    # ---------------------------------------------------------
    # Lifecycle helpers
    # ---------------------------------------------------------

    def mark_validated(self) -> EventEnvelope:
        self.status = EventStatus.VALIDATED
        return self

    def mark_processed(
        self,
        processed_at: datetime | None = None,
    ) -> EventEnvelope:
        self.status = EventStatus.PROCESSED
        self.processed_at = processed_at or datetime.now(timezone.utc)
        return self

    def mark_rejected(self) -> EventEnvelope:
        self.status = EventStatus.REJECTED
        return self

    # ---------------------------------------------------------
    # Deterministic identity
    # ---------------------------------------------------------

    @staticmethod
    def deterministic_event_id(
        *,
        chain: str,
        event_type: str,
        transaction_id: str | None = None,
        instruction_index: int | None = None,
        log_index: int | None = None,
        entity_id: str | None = None,
    ) -> str:
        """
        Generates a deterministic event ID.

        This is useful for deduplication when multiple providers report
        the same chain event.
        """

        canonical = {
            "chain": chain,
            "event_type": event_type,
            "transaction_id": transaction_id,
            "instruction_index": instruction_index,
            "log_index": log_index,
            "entity_id": entity_id,
        }

        serialized = json.dumps(
            canonical,
            sort_keys=True,
            separators=(",", ":"),
        )

        digest = hashlib.sha256(
            serialized.encode("utf-8")
        ).hexdigest()

        return f"evt_{digest[:32]}"