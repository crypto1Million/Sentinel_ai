from __future__ import annotations

import asyncio
import logging
import os
from uuid import uuid4

from config.settings import get_settings
from intelligence.orchestrator import (
    IntelligenceOrchestrator,
)
from realtime.bus import get_realtime_bus


logger = logging.getLogger(
    "sentinel.intelligence.worker"
)


class IntelligenceWorker:
    """
    Redis Stream consumer responsible for connecting
    realtime state changes to SentinelAI intelligence engines.

    One consumer group:
        sentinel-intelligence

    Multiple worker processes can safely share that group.
    Redis distributes events across consumers.
    """

    GROUP = "sentinel-intelligence"

    def __init__(self) -> None:

        self.settings = get_settings()

        self.bus = get_realtime_bus()

        self.orchestrator = (
            IntelligenceOrchestrator()
        )

        self.consumer_name = (
            f"{os.getenv('HOSTNAME', 'sentinel')}-"
            f"{os.getpid()}-"
            f"{uuid4().hex[:8]}"
        )

        self.stop_event = asyncio.Event()

    async def run(self) -> None:

        if not self.settings.REALTIME_ENABLED:
            logger.info(
                "Realtime pipeline disabled."
            )
            return

        logger.info(
            "Starting IntelligenceWorker "
            "consumer=%s group=%s",
            self.consumer_name,
            self.GROUP,
        )

        try:
            async for stream_id, event in (
                self.bus.consume(
                    group_name=self.GROUP,
                    consumer_name=self.consumer_name,
                    event_types={
                        "token.updated",
                        "wallet.updated",
                        "pool.updated",
                        "launchpad.detected",
                        "chain.observed",
                    },
                )
            ):

                if self.stop_event.is_set():
                    break

                try:
                    await self.orchestrator.handle(
                        event
                    )

                except Exception as exc:
                    logger.exception(
                        "Intelligence processing failed "
                        "stream=%s event=%s",
                        stream_id,
                        event.event_id,
                    )

                    # Publish an operational event rather
                    # than fabricating intelligence.
                    try:
                        from realtime.publisher import (
                            publish_event,
                        )

                        await publish_event(
                            event_type="system.updated",
                            entity_type="intelligence_worker",
                            entity_id=self.consumer_name,
                            chain=event.chain,
                            source="intelligence_worker",
                            source_id=event.event_id,
                            status="conflict",
                            payload={
                                "stream_id": stream_id,
                                "event_id": event.event_id,
                                "error": str(exc),
                            },
                        )
                    except Exception:
                        logger.exception(
                            "Failed to publish "
                            "intelligence worker error"
                        )

                finally:
                    # Ack after the event has been routed.
                    # Individual engines publish their own
                    # derived status/events.
                    await self.bus.ack(
                        group_name=self.GROUP,
                        stream_id=stream_id,
                    )

        except asyncio.CancelledError:
            logger.info(
                "IntelligenceWorker cancelled."
            )
            raise

        except Exception:
            logger.exception(
                "IntelligenceWorker crashed."
            )
            raise

    async def stop(self) -> None:
        self.stop_event.set()


_worker: IntelligenceWorker | None = None


def get_intelligence_worker() -> IntelligenceWorker:
    global _worker

    if _worker is None:
        _worker = IntelligenceWorker()

    return _worker