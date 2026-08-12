"""
Redis Worker Utilities
======================
"""

###############################################################################
# Imports
###############################################################################

from __future__ import annotations

import asyncio
import json
import logging
import time
from datetime import datetime, timezone

###############################################################################
# Logging
###############################################################################

logger = logging.getLogger("redis_workers")

###############################################################################
# Serialization
###############################################################################


def serialize(data):

    return json.dumps(data, default=str)


def deserialize(data):

    return json.loads(data)


###############################################################################
# Retry
###############################################################################


async def safe_execute(coroutine):

    try:

        return await coroutine()

    except Exception as exc:

        logger.exception(exc)

        return None


###############################################################################


async def retry(
    coroutine,
    retries: int = 3,
):

    for attempt in range(retries):

        try:

            return await coroutine()

        except Exception:

            if attempt == retries - 1:

                raise

            await asyncio.sleep(1)


###############################################################################
# Timing
###############################################################################


def timer():

    return time.perf_counter()


def elapsed(start):

    return time.perf_counter() - start


###############################################################################
# Payloads
###############################################################################


def worker_payload(
    worker: str,
    event: str,
):

    return {
        "worker": worker,
        "event": event,
        "timestamp": timestamp(),
    }


###############################################################################
# Runtime
###############################################################################


def timestamp():

    return datetime.now(timezone.utc).isoformat()


def diagnostics():

    return {
        "module": "redis_workers.utils",
        "timestamp": timestamp(),
    }


def summary():

    return {
        "module": "redis_workers.utils",
    }