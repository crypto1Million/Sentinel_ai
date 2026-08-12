###############################################################################
# Imports
###############################################################################

from __future__ import annotations

import json
from typing import Any

import redis

###############################################################################
# RedisRepository
###############################################################################


class RedisRepository:
    """
    Redis Repository.
    """

    ###########################################################################
    # Initialization
    ###########################################################################

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        password: str | None = None,
    ) -> None:

        self.host = host
        self.port = port
        self.db = db
        self.password = password

        self.client: redis.Redis | None = None

    ###########################################################################
    # Connection
    ###########################################################################

    def connect(self) -> None:

        self.client = redis.Redis(
            host=self.host,
            port=self.port,
            db=self.db,
            password=self.password,
            decode_responses=True,
        )

    ###########################################################################

    def disconnect(self) -> None:

        if self.client:
            self.client.close()

        self.client = None

    ###########################################################################
    # Basic Operations
    ###########################################################################

    def get(
        self,
        key: str,
    ) -> Any:

        value = self.client.get(key)

        return deserialize(value)

    ###########################################################################

    def set(
        self,
        key: str,
        value: Any,
        ttl: int | None = None,
    ) -> bool:

        value = serialize(value)

        if ttl:
            return self.client.setex(
                key,
                ttl,
                value,
            )

        return self.client.set(
            key,
            value,
        )

    ###########################################################################

    def delete(
        self,
        key: str,
    ) -> int:

        return self.client.delete(key)

    ###########################################################################

    def exists(
        self,
        key: str,
    ) -> bool:

        return bool(self.client.exists(key))

    ###########################################################################

    def expire(
        self,
        key: str,
        ttl: int,
    ) -> bool:

        return self.client.expire(
            key,
            ttl,
        )

    ###########################################################################
    # Pub/Sub
    ###########################################################################

    def publish(
        self,
        channel: str,
        message: Any,
    ) -> int:

        return self.client.publish(
            channel,
            serialize(message),
        )

    ###########################################################################

    def subscribe(
        self,
        *channels: str,
    ):

        pubsub = self.client.pubsub()

        pubsub.subscribe(*channels)

        return pubsub

    ###########################################################################
    # Counters
    ###########################################################################

    def increment(
        self,
        key: str,
        amount: int = 1,
    ) -> int:

        return self.client.incr(
            key,
            amount,
        )

    ###########################################################################

    def decrement(
        self,
        key: str,
        amount: int = 1,
    ) -> int:

        return self.client.decr(
            key,
            amount,
        )

    ###########################################################################
    # Pipeline
    ###########################################################################

    def pipeline(self):

        return self.client.pipeline()

    ###########################################################################
    # Maintenance
    ###########################################################################

    def flush(self) -> bool:

        return self.client.flushdb()

    ###########################################################################
    # Health
    ###########################################################################

    def health(self) -> bool:

        try:

            return self.client.ping()

        except Exception:

            return False

    ###########################################################################

    def diagnostics(self) -> dict:

        return {
            "repository": "Redis",
            "connected": self.client is not None,
            "healthy": self.health(),
        }


###############################################################################
# Cache
###############################################################################


def cache_wallet(
    repository: RedisRepository,
    wallet: str,
    data: dict,
    ttl: int = 300,
):

    return repository.set(
        key(f"wallet:{wallet}"),
        data,
        ttl,
    )


###############################################################################


def cache_token(
    repository: RedisRepository,
    token: str,
    data: dict,
    ttl: int = 300,
):

    return repository.set(
        key(f"token:{token}"),
        data,
        ttl,
    )


###############################################################################


def cache_graph(
    repository: RedisRepository,
    graph_id: str,
    data: dict,
    ttl: int = 300,
):

    return repository.set(
        key(f"graph:{graph_id}"),
        data,
        ttl,
    )


###############################################################################


def cache_statistics(
    repository: RedisRepository,
    stats: dict,
    ttl: int = 120,
):

    return repository.set(
        key("statistics"),
        stats,
        ttl,
    )


###############################################################################


def invalidate(
    repository: RedisRepository,
    cache_key: str,
):

    return repository.delete(cache_key)


###############################################################################
# Runtime
###############################################################################


def summary():

    return {
        "repository": "Redis",
        "supports_pubsub": True,
        "supports_cache": True,
    }


###############################################################################
# Utilities
###############################################################################


def key(
    value: str,
) -> str:

    return value


###############################################################################


def namespaced_key(
    namespace: str,
    value: str,
) -> str:

    return f"{namespace}:{value}"


###############################################################################


def serialize(
    value: Any,
) -> str:

    return json.dumps(value)


###############################################################################


def deserialize(
    value: str | None,
) -> Any:

    if value is None:
        return None

    try:
        return json.loads(value)

    except Exception:
        return value