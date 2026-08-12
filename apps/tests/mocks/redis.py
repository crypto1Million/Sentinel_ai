"""
Mock Redis Integration
======================

Fake Redis cache, Pub/Sub, Streams and distributed locks.
"""

from __future__ import annotations

import time
from collections import defaultdict, deque
from typing import Any, Dict, List


class MockRedis:

    def __init__(self):

        self.cache: Dict[str, Any] = {}

        self.expiry: Dict[str, float] = {}

        self.channels: Dict[str, List[Any]] = defaultdict(list)

        self.streams: Dict[str, deque] = defaultdict(deque)

        self.locks: Dict[str, bool] = {}

    # ------------------------------------------------------------------
    # Cache
    # ------------------------------------------------------------------

    def set(
        self,
        key: str,
        value: Any,
        ex: int | None = None,
    ):

        self.cache[key] = value

        if ex is not None:
            self.expiry[key] = time.time() + ex

        return True

    def get(
        self,
        key: str,
    ):

        if key in self.expiry:

            if time.time() >= self.expiry[key]:

                self.cache.pop(key, None)
                self.expiry.pop(key, None)

                return None

        return self.cache.get(key)

    def delete(
        self,
        key: str,
    ):

        self.cache.pop(key, None)
        self.expiry.pop(key, None)

        return True

    def exists(
        self,
        key: str,
    ):

        return self.get(key) is not None

    def expire(
        self,
        key: str,
        seconds: int,
    ):

        if key not in self.cache:
            return False

        self.expiry[key] = time.time() + seconds

        return True

    # ------------------------------------------------------------------
    # Pub/Sub
    # ------------------------------------------------------------------

    def publish(
        self,
        channel: str,
        message: Any,
    ):

        self.channels[channel].append(message)

        return len(self.channels[channel])

    def messages(
        self,
        channel: str,
    ):

        return list(self.channels[channel])

    # ------------------------------------------------------------------
    # Streams
    # ------------------------------------------------------------------

    def xadd(
        self,
        stream: str,
        event: Dict[str, Any],
    ):

        event_id = str(
            len(self.streams[stream]) + 1
        )

        self.streams[stream].append(
            {
                "id": event_id,
                "data": event,
            }
        )

        return event_id

    def xread(
        self,
        stream: str,
        count: int = 10,
    ):

        return list(
            self.streams[stream]
        )[:count]

    # ------------------------------------------------------------------
    # Locks
    # ------------------------------------------------------------------

    def acquire_lock(
        self,
        key: str,
    ):

        if self.locks.get(key):
            return False

        self.locks[key] = True

        return True

    def release_lock(
        self,
        key: str,
    ):

        self.locks.pop(key, None)

        return True

    # ------------------------------------------------------------------
    # Runtime
    # ------------------------------------------------------------------

    def diagnostics(self):

        return {
            "connected": True,
            "cache_keys": len(self.cache),
            "channels": len(self.channels),
            "streams": len(self.streams),
            "locks": len(self.locks),
        }

    def summary(self):

        return {
            "service": "mock-redis",
            "cache_keys": len(self.cache),
            "channels": len(self.channels),
            "streams": len(self.streams),
        }


def mock_redis() -> MockRedis:

    return MockRedis()