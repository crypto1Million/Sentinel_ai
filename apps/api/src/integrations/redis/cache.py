"""
Redis Cache Manager
===================

High-level cache interface used throughout Sentinel AI.
"""

###############################################################################
# Imports
###############################################################################

from __future__ import annotations

import json
from typing import Any, Dict, Optional


###############################################################################
# CacheManager
###############################################################################


class CacheManager:
    """
    High-level Redis Cache Interface.
    """

    ###########################################################################
    # Initialization
    ###########################################################################

    def __init__(
        self,
        redis_client,
        default_ttl: int = 300,
    ):

        self.redis = redis_client

        self.default_ttl = default_ttl

    ###########################################################################
    # Generic Cache
    ###########################################################################

    def get(
        self,
        key: str,
    ) -> Optional[Any]:

        value = self.redis.get(key)

        if value is None:

            return None

        try:

            return json.loads(value)

        except Exception:

            return value

    ###########################################################################

    def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None,
    ):

        ttl = ttl or self.default_ttl

        self.redis.set(
            key,
            json.dumps(value),
            ex=ttl,
        )

    ###########################################################################

    def delete(
        self,
        key: str,
    ):

        self.redis.delete(key)

    ###########################################################################

    def invalidate(
        self,
        key: str,
    ):

        self.delete(key)

    ###########################################################################
    # Wallet Cache
    ###########################################################################

    def cache_wallet(
        self,
        wallet: str,
        data: Dict,
        ttl: int = 300,
    ):

        self.set(
            f"wallet:{wallet}",
            data,
            ttl,
        )

    ###########################################################################

    def wallet(
        self,
        wallet: str,
    ):

        return self.get(
            f"wallet:{wallet}"
        )

    ###########################################################################
    # Token Cache
    ###########################################################################

    def cache_token(
        self,
        mint: str,
        data: Dict,
        ttl: int = 300,
    ):

        self.set(
            f"token:{mint}",
            data,
            ttl,
        )

    ###########################################################################

    def token(
        self,
        mint: str,
    ):

        return self.get(
            f"token:{mint}"
        )

    ###########################################################################
    # Scores
    ###########################################################################

    def cache_score(
        self,
        key: str,
        score: Dict,
        ttl: int = 120,
    ):

        self.set(
            f"score:{key}",
            score,
            ttl,
        )

    ###########################################################################

    def score(
        self,
        key: str,
    ):

        return self.get(
            f"score:{key}"
        )

    ###########################################################################
    # Graph Cache
    ###########################################################################

    def cache_graph(
        self,
        graph_id: str,
        graph: Dict,
        ttl: int = 600,
    ):

        self.set(
            f"graph:{graph_id}",
            graph,
            ttl,
        )

    ###########################################################################

    def graph(
        self,
        graph_id: str,
    ):

        return self.get(
            f"graph:{graph_id}"
        )

    ###########################################################################
    # Statistics
    ###########################################################################

    def cache_statistics(
        self,
        statistics: Dict,
        ttl: int = 60,
    ):

        self.set(
            "statistics:global",
            statistics,
            ttl,
        )

    ###########################################################################

    def statistics(self):

        return self.get(
            "statistics:global"
        )

    ###########################################################################
    # Runtime
    ###########################################################################

    def diagnostics(self):

        return {
            "component": "CacheManager",
            "default_ttl": self.default_ttl,
        }

    ###########################################################################

    def summary(self):

        return {
            "provider": "Redis",
            "component": "Cache Manager",
        }


###############################################################################
# Utilities
###############################################################################


def cache_key(
    namespace: str,
    identifier: str,
) -> str:

    return f"{namespace}:{identifier}"


###############################################################################


def cache_ttl(
    object_type: str,
) -> int:

    defaults = {
        "wallet": 300,
        "token": 300,
        "score": 120,
        "graph": 600,
        "statistics": 60,
    }

    return defaults.get(
        object_type,
        300,
    )


###############################################################################


def serialize(
    value: Any,
) -> str:

    return json.dumps(value)


###############################################################################


def deserialize(
    value: str,
) -> Any:

    return json.loads(value)