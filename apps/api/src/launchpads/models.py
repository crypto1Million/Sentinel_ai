from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class LaunchpadStatus(str, Enum):
    VERIFIED = "VERIFIED"
    UNRESOLVED = "UNRESOLVED"
    CONFLICT = "CONFLICT"
    NOT_FOUND = "NOT_FOUND"
    UNAVAILABLE = "UNAVAILABLE"


class DetectionMode(str, Enum):
    EXACT_PROGRAM = "EXACT_PROGRAM"
    EXACT_FACTORY = "EXACT_FACTORY"
    PLATFORM_CONFIG = "PLATFORM_CONFIG"
    SHARED_RAIL = "SHARED_RAIL"
    AUTHORITY_METADATA = "AUTHORITY_METADATA"


class EvidenceType(str, Enum):
    PROGRAM_ID = "PROGRAM_ID"
    FACTORY_ADDRESS = "FACTORY_ADDRESS"
    PLATFORM_CONFIG = "PLATFORM_CONFIG"
    TRANSACTION = "TRANSACTION"
    INSTRUCTION = "INSTRUCTION"
    EVENT = "EVENT"
    AUTHORITY_METADATA = "AUTHORITY_METADATA"


class LaunchpadEvidence(BaseModel):
    model_config = ConfigDict(extra="forbid")

    evidence_type: EvidenceType

    value: str

    chain: str

    transaction_signature: str | None = None

    block_number: int | None = None

    slot: int | None = None

    source: str | None = None

    observed_at: datetime | None = None

    details: dict[str, Any] = Field(default_factory=dict)


class LaunchpadObservation(BaseModel):
    """
    Canonical input to launchpad attribution.

    This object should be produced by your realtime chain decoders.
    It contains observed facts only.
    """

    model_config = ConfigDict(extra="allow")

    chain: str

    token_address: str

    transaction_signature: str | None = None

    block_number: int | None = None

    slot: int | None = None

    program_ids: list[str] = Field(default_factory=list)

    factory_address: str | None = None

    platform_config_address: str | None = None

    event_name: str | None = None

    instruction_name: str | None = None

    source: str | None = None

    commitment: str | None = None

    observed_at: datetime | None = None

    authoritative_partner_id: str | None = None

    evidence: list[LaunchpadEvidence] = Field(
        default_factory=list
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )


class LaunchpadConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str

    name: str

    chain: str

    enabled: bool = True

    detection_mode: DetectionMode

    program_ids: tuple[str, ...] = ()

    factory_addresses: tuple[str, ...] = ()

    platform_config_addresses: tuple[str, ...] = ()

    event_names: tuple[str, ...] = ()

    instruction_names: tuple[str, ...] = ()

    shared_rail: bool = False

    requires_authoritative_partner_metadata: bool = False

    priority: int = 100

    reference_url: str | None = None


class LaunchpadCandidate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    launchpad_id: str

    launchpad_name: str

    chain: str

    matched_by: DetectionMode

    matched_value: str

    priority: int

    evidence: list[LaunchpadEvidence] = Field(
        default_factory=list
    )


class LaunchpadMatch(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: LaunchpadStatus

    chain: str

    token_address: str

    launchpad_id: str | None = None

    launchpad_name: str | None = None

    rail_id: str | None = None

    candidates: list[LaunchpadCandidate] = Field(
        default_factory=list
    )

    evidence: list[LaunchpadEvidence] = Field(
        default_factory=list
    )

    reason: str | None = None

    observed_at: datetime | None = None

    transaction_signature: str | None = None