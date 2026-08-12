"""
graph_cache.py

Production Graph Cache Layer

Responsible for:

• DFS cache
• BFS cache
• Funding cache
• Shortest path cache
• Centrality cache
• Cluster cache
• Cache statistics
"""

from __future__ import annotations

# =============================================================================
# Standard Library
# =============================================================================

import copy
import logging
import time

from dataclasses import dataclass, field

from typing import (
    Any,
    Dict,
    Optional,
)

# =============================================================================
# Third Party
# =============================================================================

from cachetools import TTLCache

# =============================================================================
# Logger
# =============================================================================

logger = logging.getLogger(__name__)

# =============================================================================
# Constants
# =============================================================================

DEFAULT_CACHE_TTL = 3600          # 1 hour

DEFAULT_CACHE_SIZE = 10000

DFS_CACHE_SIZE = 25000

BFS_CACHE_SIZE = 25000

PATH_CACHE_SIZE = 50000

FUNDING_CACHE_SIZE = 50000

CENTRALITY_CACHE_SIZE = 10000

CLUSTER_CACHE_SIZE = 10000

CACHE_VERSION = "1.0.0"

# =============================================================================
# Cache Entry
# =============================================================================


@dataclass(slots=True)
class CacheEntry:
    """
    Generic cache object.
    """

    key: str

    value: Any

    created_at: float = field(
        default_factory=time.time
    )

    accessed_at: float = field(
        default_factory=time.time
    )

    ttl: int = DEFAULT_CACHE_TTL

    hits: int = 0

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    @property
    def expired(self) -> bool:

        return (
            time.time() - self.created_at
        ) > self.ttl

    def touch(self) -> None:

        self.accessed_at = time.time()

        self.hits += 1


# =============================================================================
# Graph Cache
# =============================================================================


class GraphCache:
    """
    Central cache manager for WalletDNA.
    """

    ###########################################################################
    # Constructor
    ###########################################################################

    def __init__(

        self,

        ttl: int = DEFAULT_CACHE_TTL,

        max_size: int = DEFAULT_CACHE_SIZE,

    ) -> None:

        logger.info("Initializing GraphCache...")

        self.default_ttl = ttl

        self.max_size = max_size

        self._initialize_configuration()

        self._initialize_caches()

        self._initialize_statistics()

        logger.info("GraphCache initialized.")

    ###########################################################################
    # Configuration
    ###########################################################################

    def _initialize_configuration(self):

        self.cache_version = CACHE_VERSION

        self.enable_auto_cleanup = True

        self.enable_statistics = True

        self.enable_snapshots = True

    ###########################################################################
    # Cache Initialization
    ###########################################################################

    def _initialize_caches(self):

        # ---------------------------------------------------------
        # DFS
        # ---------------------------------------------------------

        self.dfs_cache = TTLCache(

            maxsize=DFS_CACHE_SIZE,

            ttl=self.default_ttl,

        )

        # ---------------------------------------------------------
        # BFS
        # ---------------------------------------------------------

        self.bfs_cache = TTLCache(

            maxsize=BFS_CACHE_SIZE,

            ttl=self.default_ttl,

        )

        # ---------------------------------------------------------
        # Shortest Paths
        # ---------------------------------------------------------

        self.shortest_path_cache = TTLCache(

            maxsize=PATH_CACHE_SIZE,

            ttl=self.default_ttl,

        )

        # ---------------------------------------------------------
        # Funding
        # ---------------------------------------------------------

        self.funding_cache = TTLCache(

            maxsize=FUNDING_CACHE_SIZE,

            ttl=self.default_ttl,

        )

        # ---------------------------------------------------------
        # Centrality
        # ---------------------------------------------------------

        self.centrality_cache = TTLCache(

            maxsize=CENTRALITY_CACHE_SIZE,

            ttl=self.default_ttl,

        )

        # ---------------------------------------------------------
        # Cluster
        # ---------------------------------------------------------

        self.cluster_cache = TTLCache(

            maxsize=CLUSTER_CACHE_SIZE,

            ttl=self.default_ttl,

        )

    ###########################################################################
    # Statistics
    ###########################################################################

    def _initialize_statistics(self):

        self.cache_hits = 0

        self.cache_misses = 0

        self.cache_puts = 0

        self.cache_removals = 0

        self.cache_invalidations = 0

        self.cleanup_runs = 0

        self.start_time = time.time()

    ###########################################################################
    # Helpers
    ###########################################################################

    @property
    def uptime(self) -> float:

        return time.time() - self.start_time

    @property
    def total_hits(self):

        return self.cache_hits

    @property
    def total_misses(self):

        return self.cache_misses

    @property
    def total_puts(self):

        return self.cache_puts

    @property
    def total_invalidations(self):

        return self.cache_invalidations

###############################################################################
# Generic Cache Operations
###############################################################################

def get(
    self,
    cache: TTLCache,
    key: str,
) -> Optional[Any]:
    """
    Generic cache lookup.

    Returns:
        Cached object or None.
    """

    try:

        value = cache.get(key)

        if value is None:

            self.miss()

            return None

        self.hit()

        return value

    except Exception as exc:

        logger.exception(
            "Cache GET failed: %s",
            exc,
        )

        self.miss()

        return None


# ---------------------------------------------------------------------------

def put(
    self,
    cache: TTLCache,
    key: str,
    value: Any,
) -> None:
    """
    Generic cache insertion.
    """

    try:

        cache[key] = value

        self.cache_puts += 1

    except Exception as exc:

        logger.exception(
            "Cache PUT failed: %s",
            exc,
        )


# ---------------------------------------------------------------------------

def remove(
    self,
    cache: TTLCache,
    key: str,
) -> bool:
    """
    Remove cache entry.

    Returns:
        True if removed.
    """

    try:

        if key not in cache:

            return False

        del cache[key]

        self.cache_removals += 1

        return True

    except Exception as exc:

        logger.exception(
            "Cache REMOVE failed: %s",
            exc,
        )

        return False


# ---------------------------------------------------------------------------

def contains(
    self,
    cache: TTLCache,
    key: str,
) -> bool:
    """
    Check whether cache contains key.
    """

    return key in cache


# ---------------------------------------------------------------------------

def touch(
    self,
    cache: TTLCache,
    key: str,
) -> bool:
    """
    Refresh cache entry lifetime.

    TTLCache refreshes by reassigning.
    """

    if key not in cache:

        return False

    value = cache[key]

    del cache[key]

    cache[key] = value

    return True


# ---------------------------------------------------------------------------

def clear(
    self,
    cache: TTLCache,
) -> None:
    """
    Clear a single cache.
    """

    cache.clear()


# ---------------------------------------------------------------------------

def clear_all(self) -> None:
    """
    Clear every graph cache.
    """

    self.dfs_cache.clear()

    self.bfs_cache.clear()

    self.shortest_path_cache.clear()

    self.funding_cache.clear()

    self.centrality_cache.clear()

    self.cluster_cache.clear()

    logger.info(
        "All graph caches cleared."
    )

###############################################################################
# DFS Cache
###############################################################################

def cache_dfs(
    self,
    start_node: str,
    depth: int,
    result: Any,
) -> None:
    """
    Cache DFS traversal result.

    Key format:
        dfs:<node>:<depth>
    """

    key = f"dfs:{start_node}:{depth}"

    self.put(
        self.dfs_cache,
        key,
        result,
    )


# ---------------------------------------------------------------------------

def get_dfs(
    self,
    start_node: str,
    depth: int,
) -> Optional[Any]:
    """
    Retrieve cached DFS result.
    """

    key = f"dfs:{start_node}:{depth}"

    return self.get(
        self.dfs_cache,
        key,
    )


# ---------------------------------------------------------------------------

def invalidate_dfs(
    self,
    start_node: Optional[str] = None,
) -> None:
    """
    Invalidate DFS cache.

    If node is None:
        clears entire DFS cache.

    Otherwise:
        removes every DFS entry
        beginning with that node.
    """

    if start_node is None:

        self.clear(self.dfs_cache)

        self.cache_invalidations += 1

        return

    prefix = f"dfs:{start_node}:"

    keys = [

        key

        for key in self.dfs_cache.keys()

        if key.startswith(prefix)

    ]

    for key in keys:

        self.remove(
            self.dfs_cache,
            key,
        )

    self.cache_invalidations += 1


# ---------------------------------------------------------------------------

def clear_dfs(self) -> None:
    """
    Clear entire DFS cache.
    """

    self.clear(
        self.dfs_cache,
    )

    self.cache_invalidations += 1


###############################################################################
# BFS Cache
###############################################################################

def cache_bfs(
    self,
    start_node: str,
    depth: int,
    result: Any,
) -> None:
    """
    Cache BFS traversal.
    """

    key = f"bfs:{start_node}:{depth}"

    self.put(
        self.bfs_cache,
        key,
        result,
    )


# ---------------------------------------------------------------------------

def get_bfs(
    self,
    start_node: str,
    depth: int,
) -> Optional[Any]:
    """
    Retrieve cached BFS traversal.
    """

    key = f"bfs:{start_node}:{depth}"

    return self.get(
        self.bfs_cache,
        key,
    )


# ---------------------------------------------------------------------------

def invalidate_bfs(
    self,
    start_node: Optional[str] = None,
) -> None:
    """
    Invalidate BFS cache.

    None -> clear everything.
    """

    if start_node is None:

        self.clear(
            self.bfs_cache,
        )

        self.cache_invalidations += 1

        return

    prefix = f"bfs:{start_node}:"

    keys = [

        key

        for key in self.bfs_cache.keys()

        if key.startswith(prefix)

    ]

    for key in keys:

        self.remove(
            self.bfs_cache,
            key,
        )

    self.cache_invalidations += 1


# ---------------------------------------------------------------------------

def clear_bfs(self) -> None:
    """
    Clear BFS cache.
    """

    self.clear(
        self.bfs_cache,
    )

    self.cache_invalidations += 1            

###############################################################################
# Shortest Path Cache
###############################################################################

def cache_shortest_path(
    self,
    source: str,
    destination: str,
    result: Any,
) -> None:
    """
    Cache shortest path result.

    Key format:
        path:<source>:<destination>
    """

    key = f"path:{source}:{destination}"

    self.put(
        self.shortest_path_cache,
        key,
        result,
    )


# ---------------------------------------------------------------------------

def get_shortest_path(
    self,
    source: str,
    destination: str,
) -> Optional[Any]:
    """
    Retrieve cached shortest path.
    """

    key = f"path:{source}:{destination}"

    return self.get(
        self.shortest_path_cache,
        key,
    )


# ---------------------------------------------------------------------------

def invalidate_shortest_path(
    self,
    node: Optional[str] = None,
) -> None:
    """
    Invalidate shortest path cache.

    node=None -> clear everything.

    node=<wallet> -> remove all paths
    containing this wallet.
    """

    if node is None:

        self.clear(
            self.shortest_path_cache,
        )

        self.cache_invalidations += 1

        return

    keys = [

        key

        for key in self.shortest_path_cache.keys()

        if f":{node}:" in key
        or key.endswith(f":{node}")
        or key.startswith(f"path:{node}:")
    ]

    for key in keys:

        self.remove(
            self.shortest_path_cache,
            key,
        )

    self.cache_invalidations += 1


# ---------------------------------------------------------------------------

def clear_shortest_path(self) -> None:
    """
    Clear shortest path cache.
    """

    self.clear(
        self.shortest_path_cache,
    )

    self.cache_invalidations += 1


###############################################################################
# Funding Cache
###############################################################################

def cache_funding_path(
    self,
    source_wallet: str,
    destination_wallet: str,
    max_depth: int,
    result: Any,
) -> None:
    """
    Cache funding path.

    Key format:

    funding:<source>:<destination>:<depth>
    """

    key = (
        f"funding:"
        f"{source_wallet}:"
        f"{destination_wallet}:"
        f"{max_depth}"
    )

    self.put(
        self.funding_cache,
        key,
        result,
    )


# ---------------------------------------------------------------------------

def get_funding_path(
    self,
    source_wallet: str,
    destination_wallet: str,
    max_depth: int,
) -> Optional[Any]:
    """
    Retrieve funding path.
    """

    key = (
        f"funding:"
        f"{source_wallet}:"
        f"{destination_wallet}:"
        f"{max_depth}"
    )

    return self.get(
        self.funding_cache,
        key,
    )


# ---------------------------------------------------------------------------

def invalidate_funding(
    self,
    wallet: Optional[str] = None,
) -> None:
    """
    Invalidate funding cache.

    wallet=None

        Clears everything.

    wallet=<wallet>

        Removes every funding path
        involving this wallet.
    """

    if wallet is None:

        self.clear(
            self.funding_cache,
        )

        self.cache_invalidations += 1

        return

    keys = [

        key

        for key in self.funding_cache.keys()

        if f":{wallet}:" in key
        or key.endswith(f":{wallet}")
        or key.startswith(f"funding:{wallet}:")
    ]

    for key in keys:

        self.remove(
            self.funding_cache,
            key,
        )

    self.cache_invalidations += 1


# ---------------------------------------------------------------------------

def clear_funding(self) -> None:
    """
    Clear funding cache.
    """

    self.clear(
        self.funding_cache,
    )

    self.cache_invalidations += 1    

###############################################################################
# Centrality Cache
###############################################################################

def cache_centrality(
    self,
    algorithm: str,
    node_id: str,
    value: Any,
) -> None:
    """
    Cache centrality score.

    Key:
        centrality:<algorithm>:<node>
    """

    key = f"centrality:{algorithm}:{node_id}"

    self.put(
        self.centrality_cache,
        key,
        value,
    )


# ---------------------------------------------------------------------------

def get_centrality(
    self,
    algorithm: str,
    node_id: str,
) -> Optional[Any]:
    """
    Retrieve cached centrality.
    """

    key = f"centrality:{algorithm}:{node_id}"

    return self.get(
        self.centrality_cache,
        key,
    )


# ---------------------------------------------------------------------------

def invalidate_centrality(
    self,
    node_id: Optional[str] = None,
    algorithm: Optional[str] = None,
) -> None:
    """
    Invalidate centrality cache.

    Examples
    --------
    invalidate_centrality()

        -> clears entire cache

    invalidate_centrality(node)

        -> clears all algorithms for node

    invalidate_centrality(node, algorithm)

        -> clears only one score
    """

    if node_id is None:

        self.clear(self.centrality_cache)

        self.cache_invalidations += 1

        return

    keys = []

    if algorithm is None:

        prefix = f"centrality:"

        keys = [

            k

            for k in self.centrality_cache.keys()

            if k.startswith(prefix)
            and k.endswith(f":{node_id}")

        ]

    else:

        key = f"centrality:{algorithm}:{node_id}"

        if key in self.centrality_cache:

            keys = [key]

    for key in keys:

        self.remove(
            self.centrality_cache,
            key,
        )

    self.cache_invalidations += 1


# ---------------------------------------------------------------------------

def clear_centrality(self) -> None:
    """
    Clear every cached centrality score.
    """

    self.clear(
        self.centrality_cache,
    )

    self.cache_invalidations += 1


###############################################################################
# Cluster Cache
###############################################################################

def cache_cluster(
    self,
    cluster_id: str,
    cluster: Any,
) -> None:
    """
    Cache cluster object.
    """

    key = f"cluster:{cluster_id}"

    self.put(
        self.cluster_cache,
        key,
        cluster,
    )


# ---------------------------------------------------------------------------

def get_cluster(
    self,
    cluster_id: str,
) -> Optional[Any]:
    """
    Retrieve cached cluster.
    """

    key = f"cluster:{cluster_id}"

    return self.get(
        self.cluster_cache,
        key,
    )


# ---------------------------------------------------------------------------

def invalidate_cluster(
    self,
    cluster_id: Optional[str] = None,
) -> None:
    """
    Invalidate cluster cache.

    cluster_id=None

        clears everything.
    """

    if cluster_id is None:

        self.clear(
            self.cluster_cache,
        )

        self.cache_invalidations += 1

        return

    key = f"cluster:{cluster_id}"

    self.remove(
        self.cluster_cache,
        key,
    )

    self.cache_invalidations += 1


# ---------------------------------------------------------------------------

def clear_cluster(self) -> None:
    """
    Clear cluster cache.
    """

    self.clear(
        self.cluster_cache,
    )

    self.cache_invalidations += 1


###############################################################################
# Cache Sizes
###############################################################################

@property
def centrality_cache_size(self) -> int:

    return len(self.centrality_cache)


@property
def cluster_cache_size(self) -> int:

    return len(self.cluster_cache)

###############################################################################
# Expiration
###############################################################################

def cleanup_expired(self) -> int:
    """
    Cleanup expired entries.

    TTLCache removes expired items lazily.
    This forces cleanup.

    Returns:
        Number of expired entries removed.
    """

    removed = 0

    caches = [

        self.dfs_cache,
        self.bfs_cache,
        self.shortest_path_cache,
        self.funding_cache,
        self.centrality_cache,
        self.cluster_cache,

    ]

    for cache in caches:

        before = len(cache)

        # trigger expiration
        list(cache.keys())

        after = len(cache)

        removed += before - after

    self.cleanup_runs += 1

    logger.info(
        "Expired cache entries removed: %d",
        removed,
    )

    return removed


# ---------------------------------------------------------------------------

def is_expired(
    self,
    cache: TTLCache,
    key: str,
) -> bool:
    """
    Returns True if key does not exist
    (expired or never inserted).
    """

    return key not in cache


# ---------------------------------------------------------------------------

def ttl_remaining(
    self,
    cache: TTLCache,
    key: str,
) -> Optional[int]:
    """
    TTLCache doesn't expose remaining TTL.

    Returns None if unavailable.
    """

    if key not in cache:

        return None

    return self.default_ttl


###############################################################################
# Statistics
###############################################################################

def hit(self) -> None:

    self.cache_hits += 1


# ---------------------------------------------------------------------------

def miss(self) -> None:

    self.cache_misses += 1


# ---------------------------------------------------------------------------

def reset_statistics(self) -> None:

    self.cache_hits = 0

    self.cache_misses = 0

    self.cache_puts = 0

    self.cache_removals = 0

    self.cache_invalidations = 0

    self.cleanup_runs = 0


# ---------------------------------------------------------------------------

def statistics(self) -> Dict[str, Any]:
    """
    Returns complete cache statistics.
    """

    total_requests = self.cache_hits + self.cache_misses

    hit_rate = (

        self.cache_hits / total_requests

        if total_requests

        else 0.0

    )

    return {

        "version": self.cache_version,

        "uptime": self.uptime,

        "hits": self.cache_hits,

        "misses": self.cache_misses,

        "hit_rate": hit_rate,

        "puts": self.cache_puts,

        "removals": self.cache_removals,

        "invalidations": self.cache_invalidations,

        "cleanup_runs": self.cleanup_runs,

        "dfs_entries": len(self.dfs_cache),

        "bfs_entries": len(self.bfs_cache),

        "path_entries": len(self.shortest_path_cache),

        "funding_entries": len(self.funding_cache),

        "centrality_entries": len(self.centrality_cache),

        "cluster_entries": len(self.cluster_cache),

    }


# ---------------------------------------------------------------------------

def memory_usage(self) -> Dict[str, int]:
    """
    Approximate memory usage.
    """

    return {

        "dfs": self.dfs_cache.__sizeof__(),

        "bfs": self.bfs_cache.__sizeof__(),

        "paths": self.shortest_path_cache.__sizeof__(),

        "funding": self.funding_cache.__sizeof__(),

        "centrality": self.centrality_cache.__sizeof__(),

        "cluster": self.cluster_cache.__sizeof__(),

        "total":

            self.dfs_cache.__sizeof__()

            + self.bfs_cache.__sizeof__()

            + self.shortest_path_cache.__sizeof__()

            + self.funding_cache.__sizeof__()

            + self.centrality_cache.__sizeof__()

            + self.cluster_cache.__sizeof__(),

    }


###############################################################################
# Snapshot / Restore
###############################################################################

def snapshot(self) -> Dict[str, Any]:
    """
    Deep snapshot of all caches.
    """

    return {

        "dfs": copy.deepcopy(dict(self.dfs_cache)),

        "bfs": copy.deepcopy(dict(self.bfs_cache)),

        "paths": copy.deepcopy(dict(self.shortest_path_cache)),

        "funding": copy.deepcopy(dict(self.funding_cache)),

        "centrality": copy.deepcopy(dict(self.centrality_cache)),

        "cluster": copy.deepcopy(dict(self.cluster_cache)),

    }


# ---------------------------------------------------------------------------

def restore(
    self,
    snapshot: Dict[str, Any],
) -> None:
    """
    Restore caches.
    """

    self.clear_all()

    self.dfs_cache.update(snapshot.get("dfs", {}))

    self.bfs_cache.update(snapshot.get("bfs", {}))

    self.shortest_path_cache.update(

        snapshot.get("paths", {})

    )

    self.funding_cache.update(

        snapshot.get("funding", {})

    )

    self.centrality_cache.update(

        snapshot.get("centrality", {})

    )

    self.cluster_cache.update(

        snapshot.get("cluster", {})

    )

    logger.info("Cache restored.")


###############################################################################
# Export / Import
###############################################################################

def export(self) -> Dict[str, Any]:
    """
    Export cache contents.
    """

    return self.snapshot()


# ---------------------------------------------------------------------------

def import_cache(
    self,
    data: Dict[str, Any],
) -> None:
    """
    Import cache.
    """

    self.restore(data)

    logger.info("Cache imported.")        