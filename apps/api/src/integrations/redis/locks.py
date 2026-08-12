"""
Redis Distributed Lock Manager
==============================
"""

from __future__ import annotations

import time
from typing import Optional


class LockManager:
    """
    Distributed lock abstraction.
    """

    ###########################################################################
    # Initialization
    ###########################################################################

    def __init__(
        self,
        redis_client,
    ):

        self.redis = redis_client

    ###########################################################################
    # Lock Operations
    ###########################################################################

    def acquire(
        self,
        name: str,
        timeout: int = 30,
        blocking: bool = True,
    ):

        lock = self.redis.connection.lock(
            name,
            timeout=timeout,
        )

        success = lock.acquire(
            blocking=blocking,
        )

        if success:

            return lock

        return None

    ###########################################################################

    def release(
        self,
        lock,
    ):

        if lock:

            lock.release()

    ###########################################################################

    def locked(
        self,
        name: str,
    ) -> bool:

        return self.redis.connection.exists(
            name,
        ) > 0

    ###########################################################################

    def wait(
        self,
        name: str,
        interval: float = 0.5,
    ):

        while self.locked(name):

            time.sleep(interval)

    ###########################################################################

    def force_release(
        self,
        name: str,
    ):

        self.redis.connection.delete(name)

    ###########################################################################
    # Runtime
    ###########################################################################

    def diagnostics(self):

        return {
            "component": "LockManager",
        }

    ###########################################################################

    def summary(self):

        return {
            "provider": "Redis Locks",
        }


###############################################################################
# Utilities
###############################################################################


def lock_key(
    resource: str,
) -> str:

    return f"lock:{resource}"


###############################################################################


def lock_metadata(
    resource: str,
) -> dict:

    return {
        "resource": resource,
        "lock_key": lock_key(resource),
    }