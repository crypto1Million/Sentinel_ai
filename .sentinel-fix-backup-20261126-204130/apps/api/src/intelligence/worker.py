from __future__ import annotations

import logging
import os
from uuid import uuid4

from config.settings import get_settings

from intelligence.orchestrator import (
    IntelligenceOrchestrator,
)

from realtime.bus import get_realtime_bus
from realtime.publisher import publish_event
from realtime.state_processor import StateProcessor


logger = logging.getLogger(
    "sentinel.intelligence.worker"
)


class IntelligenceWorker:
    """Single ordered consumer for the SentinelAI event pipeline."""

    GROUP = "sentinel-pipeline"

    def __init__(self) -> None:
        self.settings = get_settings()
        self.bus = get_realtime_bus()

        self.state_processor = StateProcessor()

        self.orchestrator = IntelligenceOrchestrator(
            state_service=self.state_processor.state
        )

        self.consumer_name = (
            f"{os.getenv('HOSTNAME', 'sentinel')}-"
            f"{os.getpid()}-{uuid4().hex[:8]}"
        )

    async def _process(
        self,
        stream_id: str,
        event,
    ) -> None:
        # State must be updated before intelligence reads it.
        await self.state_processor.process(event)

        await self.orchestrator.handle(event)

        await self.bus.ack(
            group_name=self.GROUP,
            stream_id=stream_id,
        )

    async def run(self) -> None:
        if not self.settings.REALTIME_ENABLED:
            logger.warning(
                "Realtime pipeline disabled."
            )
            return

        event_types = {
            "token.updated",
            "wallet.updated",
            "pool.updated",
            "launchpad.detected",
            "chain.observed",
        }

        logger.info(
            "Starting event worker consumer=%s",
            self.consumer_name,
        )

        # Recover events left pending by a crashed worker.
        async for stream_id, event in self.bus.recover_pending(
            group_name=self.GROUP,
            consumer_name=self.consumer_name,
            min_idle_ms=0,
            count=100,
        ):
            await self._process(stream_id, event)

        async for stream_id, event in self.bus.consume(
            group_name=self.GROUP,
            consumer_name=self.consumer_name,
            event_types=event_types,
        ):
            try:
                await self._process(stream_id, event)

            except Exception as exc:
                logger.exception(
                    "Pipeline processing failed: %s",
                    stream_id,
                )

                await publish_event(
                    event_type="system.updated",
                    entity_type="pipeline_worker",
                    entity_id=self.consumer_name,
                    chain=event.chain,
                    source="pipeline_worker",
                    source_id=event.event_id,
                    status="error",
                    payload={
                        "failed_stream_id": stream_id,
                        "failed_event_id": event.event_id,
                        "error": str(exc),
                    },
                )

                # Failed message remains pending for recovery.
                raise