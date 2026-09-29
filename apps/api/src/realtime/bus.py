from __future__ import annotations

import asyncio
import json
from collections.abc import AsyncIterator
from typing import Any

from redis.asyncio import Redis
from redis.exceptions import ResponseError

from config.settings import get_settings
from realtime.models import RealtimeEvent


class RealtimeBus:
    """
    SentinelAI's canonical Redis Streams event bus.

    Architecture:

        Producers
            ↓
        XADD
            ↓
        sentinel:events
            ↓
        ┌───────────────┬─────────────────┐
        │               │                 │
     Backend       WebSocket         Replay /
     workers       gateways          recovery

    Important:
    - Redis Streams are durable until trimmed/expired.
    - Backend workers should use consumer groups.
    - WebSocket clients should use independent stream cursors,
      NOT one shared consumer group, otherwise clients would
      steal events from each other.
    """

    def __init__(
        self,
        redis_client: Redis | None = None,
    ) -> None:
        self.settings = get_settings()

        self.redis: Redis = (
            redis_client
            if redis_client is not None
            else Redis.from_url(
                self._redis_url(),
                decode_responses=True,
                health_check_interval=30,
            )
        )

        self.stream_name = (
            f"{self.settings.REDIS_STREAM_PREFIX}:"
            f"{self.settings.REDIS_EVENT_STREAM}"
        )

        self.max_len = (
            self.settings.REDIS_STREAM_MAXLEN
        )

        self.block_ms = (
            self.settings.REDIS_STREAM_BLOCK_MS
        )

        self.read_count = (
            self.settings.REDIS_STREAM_READ_COUNT
        )

        self._group_lock = asyncio.Lock()

    # =========================================================
    # REDIS CONNECTION
    # =========================================================

    def _redis_url(self) -> str:
        password = self.settings.REDIS_PASSWORD

        if password:
            return (
                "redis://:"
                f"{password}@"
                f"{self.settings.REDIS_HOST}:"
                f"{self.settings.REDIS_PORT}/"
                f"{self.settings.REDIS_DB}"
            )

        return (
            "redis://"
            f"{self.settings.REDIS_HOST}:"
            f"{self.settings.REDIS_PORT}/"
            f"{self.settings.REDIS_DB}"
        )

    # =========================================================
    # STREAM HELPERS
    # =========================================================

    async def ensure_group(
        self,
        group_name: str,
        *,
        start_id: str = "0-0",
    ) -> None:
        """
        Create a consumer group if it does not already exist.
        """

        async with self._group_lock:
            try:
                await self.redis.xgroup_create(
                    name=self.stream_name,
                    groupname=group_name,
                    id=start_id,
                    mkstream=True,
                )

            except ResponseError as exc:
                # BUSYGROUP means the group already exists.
                if "BUSYGROUP" not in str(exc):
                    raise

    # =========================================================
    # PUBLISH
    # =========================================================

    async def publish(
        self,
        event: RealtimeEvent,
    ) -> str:
        """
        Append an event to the canonical Redis Stream.

        Returns:
            Redis Stream ID, e.g. "1758978123456-0"
        """

        processed_event = (
            event.with_processed_timestamp()
        )

        payload = json.dumps(
            processed_event.to_wire(),
            default=str,
            separators=(",", ":"),
        )

        stream_id = await self.redis.xadd(
            name=self.stream_name,
            fields={
                "event": payload,
            },
            maxlen=self.max_len,
            approximate=True,
        )

        return str(stream_id)

    # =========================================================
    # READ FOR WEBSOCKET / FAN-OUT
    # =========================================================

    async def subscribe(
        self,
        *,
        event_types: set[str] | None = None,
        last_id: str = "$",
    ) -> AsyncIterator[RealtimeEvent]:
        """
        Read events using an independent Redis Stream cursor.

        This is intentionally NOT a consumer group.

        Every WebSocket connection gets its own cursor, so all
        connected clients can receive the same event.

        Args:
            event_types:
                Optional set such as {"token.updated"}.
            last_id:
                "$" starts from events arriving after subscription.
                "0-0" replays from the beginning of the retained stream.
                A Redis Stream ID resumes after a known checkpoint.
        """

        cursor = last_id

        while True:
            results = await self.redis.xread(
                streams={
                    self.stream_name: cursor,
                },
                count=self.read_count,
                block=self.block_ms,
            )

            if not results:
                continue

            for _stream_name, messages in results:
                for stream_id, fields in messages:
                    cursor = str(stream_id)

                    raw_event = fields.get("event")

                    if not raw_event:
                        continue

                    try:
                        event = (
                            RealtimeEvent.model_validate_json(
                                raw_event
                            )
                        )
                    except Exception:
                        # A malformed event must not terminate
                        # every realtime subscriber.
                        continue

                    if (
                        event_types
                        and event.event_type
                        not in event_types
                    ):
                        continue

                    yield event

    # =========================================================
    # CONSUMER GROUPS
    # =========================================================

    async def consume(
        self,
        *,
        group_name: str,
        consumer_name: str,
        event_types: set[str] | None = None,
        count: int | None = None,
        block_ms: int | None = None,
    ) -> AsyncIterator[
        tuple[str, RealtimeEvent]
    ]:
        """
        Consume events through a Redis Stream consumer group.

        Multiple workers sharing the same group will distribute
        events between themselves.

        Returns:
            (stream_id, event)
        """

        await self.ensure_group(
            group_name=group_name,
            start_id="0-0",
        )

        read_count = (
            count
            if count is not None
            else self.read_count
        )

        read_block = (
            block_ms
            if block_ms is not None
            else self.block_ms
        )

        while True:
            results = await self.redis.xreadgroup(
                groupname=group_name,
                consumername=consumer_name,
                streams={
                    self.stream_name: ">",
                },
                count=read_count,
                block=read_block,
            )

            if not results:
                continue

            for _stream_name, messages in results:
                for stream_id, fields in messages:
                    raw_event = fields.get("event")

                    if not raw_event:
                        await self.ack(
                            group_name=group_name,
                            stream_id=str(stream_id),
                        )
                        continue

                    try:
                        event = (
                            RealtimeEvent.model_validate_json(
                                raw_event
                            )
                        )
                    except Exception:
                        await self.ack(
                            group_name=group_name,
                            stream_id=str(stream_id),
                        )
                        continue

                    if (
                        event_types
                        and event.event_type
                        not in event_types
                    ):
                        await self.ack(
                            group_name=group_name,
                            stream_id=str(stream_id),
                        )
                        continue

                    yield (
                        str(stream_id),
                        event,
                    )

    # =========================================================
    # ACK
    # =========================================================

    async def ack(
        self,
        *,
        group_name: str,
        stream_id: str,
    ) -> int:
        """
        Acknowledge successful processing of one event.
        """

        return int(
            await self.redis.xack(
                self.stream_name,
                group_name,
                stream_id,
            )
        )

    # =========================================================
    # PENDING / RECOVERY
    # =========================================================

    async def recover_pending(
        self,
        *,
        group_name: str,
        consumer_name: str,
        min_idle_ms: int = 30_000,
        count: int = 100,
    ) -> AsyncIterator[
        tuple[str, RealtimeEvent]
    ]:
        """
        Recover events that were delivered to a worker but
        never ACKed.

        This protects SentinelAI against worker crashes.
        """

        try:
            pending = await self.redis.xautoclaim(
                name=self.stream_name,
                groupname=group_name,
                consumername=consumer_name,
                min_idle_time=min_idle_ms,
                start_id="0-0",
                count=count,
            )
        except ResponseError:
            return

        # redis-py returns:
        # (next_start_id, messages, deleted_ids)
        if not pending:
            return

        _next_start_id, messages, _deleted = pending

        for stream_id, fields in messages:
            raw_event = fields.get("event")

            if not raw_event:
                await self.ack(
                    group_name=group_name,
                    stream_id=str(stream_id),
                )
                continue

            try:
                event = (
                    RealtimeEvent.model_validate_json(
                        raw_event
                    )
                )
            except Exception:
                await self.ack(
                    group_name=group_name,
                    stream_id=str(stream_id),
                )
                continue

            yield (
                str(stream_id),
                event,
            )

    # =========================================================
    # REPLAY
    # =========================================================

    async def replay(
        self,
        *,
        start_id: str = "-",
        end_id: str = "+",
        count: int = 1000,
        event_types: set[str] | None = None,
    ) -> list[
        tuple[str, RealtimeEvent]
    ]:
        """
        Read retained historical events without consuming them.

        Useful for:
        - ReplayTimeline
        - debugging
        - backtesting
        - recomputation
        """

        messages = await self.redis.xrange(
            name=self.stream_name,
            min=start_id,
            max=end_id,
            count=count,
        )

        output: list[
            tuple[str, RealtimeEvent]
        ] = []

        for stream_id, fields in messages:
            raw_event = fields.get("event")

            if not raw_event:
                continue

            try:
                event = (
                    RealtimeEvent.model_validate_json(
                        raw_event
                    )
                )
            except Exception:
                continue

            if (
                event_types
                and event.event_type
                not in event_types
            ):
                continue

            output.append(
                (
                    str(stream_id),
                    event,
                )
            )

        return output

    # =========================================================
    # LATEST EVENT
    # =========================================================

    async def latest(
        self,
    ) -> tuple[str, RealtimeEvent] | None:
        """
        Return the most recent retained event.
        """

        messages = await self.redis.xrevrange(
            name=self.stream_name,
            max="+",
            min="-",
            count=1,
        )

        if not messages:
            return None

        stream_id, fields = messages[0]

        raw_event = fields.get("event")

        if not raw_event:
            return None

        try:
            event = (
                RealtimeEvent.model_validate_json(
                    raw_event
                )
            )
        except Exception:
            return None

        return (
            str(stream_id),
            event,
        )

    # =========================================================
    # HEALTH
    # =========================================================

    async def ping(self) -> bool:
        try:
            return bool(
                await self.redis.ping()
            )
        except Exception:
            return False

    # =========================================================
    # SHUTDOWN
    # =========================================================

    async def close(self) -> None:
        """
        Close the process-level Redis connection.

        Individual subscribers MUST NOT call this.
        """

        await self.redis.aclose()


_bus: RealtimeBus | None = None


def get_realtime_bus() -> RealtimeBus:
    """
    Return the process-local SentinelAI realtime bus.
    """

    global _bus

    if _bus is None:
        _bus = RealtimeBus()

    return _bus