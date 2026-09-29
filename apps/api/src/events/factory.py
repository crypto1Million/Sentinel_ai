from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from events.models import CanonicalEventModel
from realtime.envelope import (
    ChainPosition,
    DataQuality,
    EventEnvelope,
    EventStatus,
    ParserMetadata,
    SourceMetadata,
)


def build_event(
    *,
    event_type: str,
    chain: str,
    entity_type: str,
    entity_id: str,
    payload: CanonicalEventModel | dict[str, Any],
    source: SourceMetadata,
    parser_name: str,
    parser_version: str,
    chain_position: ChainPosition | None = None,
    evidence: list[dict[str, Any]] | None = None,
    quality: DataQuality = DataQuality.VERIFIED,
    correlation_id: str | None = None,
    parent_event_ids: list[str] | None = None,
    raw_payload: dict[str, Any] | None = None,
    metadata: dict[str, Any] | None = None,
) -> EventEnvelope:

    observed_at = (
        source.observed_at
        or datetime.now(timezone.utc)
    )

    transaction_id = None
    instruction_index = None
    log_index = None

    if chain_position:
        transaction_id = (
            chain_position.transaction_signature
            or chain_position.transaction_hash
        )

        instruction_index = (
            chain_position.instruction_index
        )

        log_index = chain_position.log_index

    event_id = EventEnvelope.deterministic_event_id(
        chain=chain,
        event_type=event_type,
        transaction_id=transaction_id,
        instruction_index=instruction_index,
        log_index=log_index,
        entity_id=entity_id,
    )

    if isinstance(payload, CanonicalEventModel):
        normalized_payload = payload.model_dump(
            mode="json"
        )
    else:
        normalized_payload = payload

    normalized_evidence = evidence or []

    return EventEnvelope(
        event_id=event_id,
        event_type=event_type,
        chain=chain,
        entity_type=entity_type,
        entity_id=entity_id,
        observed_at=observed_at,
        chain_position=chain_position,
        source=source,
        parser=ParserMetadata(
            name=parser_name,
            version=parser_version,
        ),
        evidence=normalized_evidence,
        status=EventStatus.RECEIVED,
        quality=quality,
        payload=normalized_payload,
        raw_payload=raw_payload,
        correlation_id=correlation_id,
        parent_event_ids=parent_event_ids or [],
        metadata=metadata or {},
    )