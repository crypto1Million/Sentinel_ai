from __future__ import annotations

from typing import Any

from realtime.bus import get_realtime_bus
from realtime.models import RealtimeEvent


async def publish_event(
    *,
    event_type: str,
    entity_type: str,
    entity_id: str,
    payload: dict[str, Any],
    source: str,
    source_id: str | None = None,
    chain: str | None = None,
    status: str = "observed",
) -> RealtimeEvent:
    """
    Publish one canonical SentinelAI realtime event.

    This is the entry point that future ingestion,
    intelligence, scoring and alert services should use.
    """

    event = RealtimeEvent(
        event_type=event_type,
        entity_type=entity_type,
        entity_id=entity_id,
        chain=chain,
        payload=payload,
        source=source,
        source_id=source_id,
        status=status,
    )

    await get_realtime_bus().publish(
        event
    )

    return event