"""
Redis Streams Manager
=====================

Redis Streams abstraction for Sentinel AI.
"""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional


class StreamManager:
    """
    Redis Streams interface.
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
    # Stream Operations
    ###########################################################################

    def create_stream(
        self,
        stream: str,
    ):

        return stream

    ###########################################################################

    def add(
        self,
        stream: str,
        data: Dict,
        maxlen: Optional[int] = None,
    ):

        payload = serialize(data)

        return self.redis.connection.xadd(
            stream,
            payload,
            maxlen=maxlen,
            approximate=True,
        )

    ###########################################################################

    def read(
        self,
        streams: Dict,
        count: int = 100,
        block: int = 0,
    ):

        return self.redis.connection.xread(
            streams,
            count=count,
            block=block,
        )

    ###########################################################################

    def create_group(
        self,
        stream: str,
        group: str,
    ):

        return self.redis.connection.xgroup_create(
            stream,
            group,
            id="0",
            mkstream=True,
        )

    ###########################################################################

    def read_group(
        self,
        group: str,
        consumer: str,
        streams: Dict,
        count: int = 100,
        block: int = 0,
    ):

        return self.redis.connection.xreadgroup(
            group,
            consumer,
            streams,
            count=count,
            block=block,
        )

    ###########################################################################

    def acknowledge(
        self,
        stream: str,
        group: str,
        *ids,
    ):

        return self.redis.connection.xack(
            stream,
            group,
            *ids,
        )

    ###########################################################################

    def pending(
        self,
        stream: str,
        group: str,
    ):

        return self.redis.connection.xpending(
            stream,
            group,
        )

    ###########################################################################

    def delete(
        self,
        stream: str,
        *ids,
    ):

        return self.redis.connection.xdel(
            stream,
            *ids,
        )

    ###########################################################################

    def trim(
        self,
        stream: str,
        maxlen: int,
    ):

        return self.redis.connection.xtrim(
            stream,
            maxlen=maxlen,
            approximate=True,
        )

    ###########################################################################

    def info(
        self,
        stream: str,
    ):

        return self.redis.connection.xinfo_stream(
            stream,
        )

    ###########################################################################
    # Runtime
    ###########################################################################

    def diagnostics(self):

        return {
            "component": "StreamManager",
        }

    ###########################################################################

    def summary(self):

        return {
            "provider": "Redis Streams",
        }


###############################################################################
# Utilities
###############################################################################


def serialize(
    data: Dict,
) -> Dict:

    return {
        k: json.dumps(v)
        if isinstance(v, (dict, list))
        else str(v)
        for k, v in data.items()
    }


###############################################################################


def deserialize(
    data: Dict,
) -> Dict:

    result = {}

    for k, v in data.items():

        try:

            result[k] = json.loads(v)

        except Exception:

            result[k] = v

    return result