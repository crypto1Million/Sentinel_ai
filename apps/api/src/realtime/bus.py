from __future__ import annotations

import json
from collections.abc import AsyncIterator

from redis.asyncio import Redis

from config.settings import get_settings
from realtime.models import RealtimeEvent


class RealtimeBus:
    """
    Central SentinelAI realtime event bus.

    Domain services publish events here.
    WebSocket consumers subscribe here.

    Redis is used only as the transport layer.
    Domain logic remains outside this class.
    """

    CHANNEL_PREFIX = "sentinel:realtime"

    def __init__(
        self,
        redis_client: Redis | None = None,
    ) -> None:
        self.settings = get_settings()

        self.redis = (
            redis_client
            or Redis.from_url(
                self._redis_url(),
                decode_responses=True,
            )
        )

    def _redis_url(self) -> str:
        password = (
            self.settings.REDIS_PASSWORD
        )

        if password:
            return (
                "redis://:"
                f"{password}@"
                f"{self.settings.REDIS_HOST}:"
                f"{self.settings.REDIS_PORT}/0"
            )

        return (
            f"redis://"
            f"{self.settings.REDIS_HOST}:"
            f"{self.settings.REDIS_PORT}/0"
        )

    @classmethod
    def channel(
        cls,
        event_type: str,
    ) -> str:
        return (
            f"{cls.CHANNEL_PREFIX}:"
            f"{event_type}"
        )

    @classmethod
    def pattern(cls) -> str:
        return (
            f"{cls.CHANNEL_PREFIX}:*"
        )

    async def publish(
        self,
        event: RealtimeEvent,
    ) -> int:
        """
        Publish a canonical event.

        Returns the number of Redis subscribers that
        received the message.
        """

        processed_event = (
            event.with_processed_timestamp()
        )

        message = json.dumps(
            processed_event.to_wire(),
            default=str,
            separators=(
                ",",
                ":",
            ),
        )

        return await self.redis.publish(
            self.channel(
                processed_event.event_type
            ),
            message,
        )

    async def subscribe(
        self,
        *,
        event_types: set[str] | None = None,
    ) -> AsyncIterator[RealtimeEvent]:
        """
        Subscribe to selected realtime event types.

        When event_types is None, subscribe to every
        SentinelAI realtime event.
        """

        pubsub = self.redis.pubsub()

        try:
            if event_types:
                channels = [
                    self.channel(
                        event_type
                    )
                    for event_type in event_types
                ]

                await pubsub.subscribe(
                    *channels
                )
            else:
                await pubsub.psubscribe(
                    self.pattern()
                )

            async for message in pubsub.listen():
                message_type = message.get(
                    "type"
                )

                if message_type not in {
                    "message",
                    "pmessage",
                }:
                    continue

                raw_data = message.get(
                    "data"
                )

                if not raw_data:
                    continue

                try:
                    yield RealtimeEvent.model_validate_json(
                        raw_data
                    )
                except Exception:
                    # Bad messages must never kill
                    # the websocket consumer.
                    continue

        finally:
            try:
                await pubsub.close()
            finally:
                await self.redis.aclose()

    async def ping(self) -> bool:
        """
        Verify the realtime transport is available.
        """
        try:
            return bool(
                await self.redis.ping()
            )
        except Exception:
            return False

    async def close(self) -> None:
        await self.redis.aclose()


_bus: RealtimeBus | None = None


def get_realtime_bus() -> RealtimeBus:
    """
    Return the process-local realtime bus instance.
    """
    global _bus

    if _bus is None:
        _bus = RealtimeBus()

    return _bus