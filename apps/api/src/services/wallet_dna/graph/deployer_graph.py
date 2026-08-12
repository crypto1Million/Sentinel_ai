# ============================================================================
# Graph Backend
# ============================================================================

from __future__ import annotations

import logging
from typing import Optional

import networkx as nx

try:
    import rustworkx as rx

    RUSTWORKX_AVAILABLE = True

except ImportError:
    rx = None
    RUSTWORKX_AVAILABLE = False


class GraphBackend:
    """
    Wrapper around NetworkX / Rustworkx.

    NetworkX:
        - Easy debugging
        - Rich algorithms
        - Visualization

    Rustworkx:
        - Much faster
        - Lower memory usage
        - Production backend
    """

    def __init__(
        self,
        backend: str = "networkx",
        directed: bool = True,
    ) -> None:

        self.logger = logging.getLogger(__name__)

        self.backend = backend.lower()

        self.directed = directed

        self.graph: Optional[object] = None

        self._initialize()

    # --------------------------------------------------------------------- #

    def _initialize(self) -> None:

        if self.backend == "rustworkx":

            if not RUSTWORKX_AVAILABLE:

                self.logger.warning(
                    "Rustworkx not installed. Falling back to NetworkX."
                )

                self.backend = "networkx"

            else:

                self.graph = (
                    rx.PyDiGraph()
                    if self.directed
                    else rx.PyGraph()
                )

                self.logger.info(
                    "Rustworkx backend initialized."
                )

                return

        # Default

        self.graph = (
            nx.DiGraph()
            if self.directed
            else nx.Graph()
        )

        self.logger.info(
            "NetworkX backend initialized."
        )

    # --------------------------------------------------------------------- #

    @property
    def is_networkx(self) -> bool:

        return self.backend == "networkx"

    @property
    def is_rustworkx(self) -> bool:

        return self.backend == "rustworkx"

class DeployerGraph:

    def __init__(self):

        self.backend = GraphBackend(
            backend="rustworkx",
            directed=True,
        )

        self.graph = self.backend.graph        


# ============================================================================
# Node Storage
# ============================================================================

# --------------------------------------------------------------------------
# Wallet Nodes
# --------------------------------------------------------------------------

# Primary wallet storage
self.wallet_nodes: Dict[str, WalletNode] = {}

# Wallet ID → Address
self.wallet_id_map: Dict[int, str] = {}

# Address → Graph Node Index
self.wallet_graph_index: Dict[str, int] = {}

# Wallet labels
self.wallet_labels: Dict[str, Set[str]] = defaultdict(set)

# Wallet metadata cache
self.wallet_metadata: Dict[str, Dict[str, Any]] = {}

# --------------------------------------------------------------------------
# Token Nodes
# --------------------------------------------------------------------------

# Mint → TokenNode
self.token_nodes: Dict[str, TokenNode] = {}

# Graph Index
self.token_graph_index: Dict[str, int] = {}

# Token metadata
self.token_metadata: Dict[str, Dict[str, Any]] = {}

# --------------------------------------------------------------------------
# Universal Node Registry
# --------------------------------------------------------------------------

# Every node inside graph
# Key:
# wallet:<address>
# token:<mint>

self.node_registry: Dict[str, Union[WalletNode, TokenNode]] = {}

# Graph Node ID
self.node_index: Dict[str, int] = {}

# Reverse lookup
self.reverse_node_index: Dict[int, str] = {}        

# ============================================================================
# Edge Storage
# ============================================================================

# --------------------------------------------------------------------------
# Funding Edges
# --------------------------------------------------------------------------

# Edge ID -> FundingEdge
self.funding_edges: Dict[str, FundingEdge] = {}

# Source Wallet -> Funding Edge IDs
self.funding_outgoing: Dict[str, Set[str]] = defaultdict(set)

# Destination Wallet -> Funding Edge IDs
self.funding_incoming: Dict[str, Set[str]] = defaultdict(set)

# --------------------------------------------------------------------------
# Deployment Edges
# --------------------------------------------------------------------------

# Edge ID -> DeploymentEdge
self.deployment_edges: Dict[str, DeploymentEdge] = {}

# Wallet -> Deployment Edge IDs
self.deployment_index: Dict[str, Set[str]] = defaultdict(set)

# Token -> Deployment Edge IDs
self.token_deployment_index: Dict[str, Set[str]] = defaultdict(set)

# --------------------------------------------------------------------------
# Transfer Edges
# --------------------------------------------------------------------------

# Edge ID -> TransferEdge
self.transfer_edges: Dict[str, TransferEdge] = {}

# Wallet -> Transfer Edge IDs
self.transfer_outgoing: Dict[str, Set[str]] = defaultdict(set)

# Wallet -> Incoming Transfer IDs
self.transfer_incoming: Dict[str, Set[str]] = defaultdict(set)

# --------------------------------------------------------------------------
# Bundle Edges
# --------------------------------------------------------------------------

# Bundle ID -> BundleEdge
self.bundle_edges: Dict[str, BundleEdge] = {}

# Wallet -> Bundle IDs
self.bundle_index: Dict[str, Set[str]] = defaultdict(set)

# --------------------------------------------------------------------------
# Interaction Edges
# --------------------------------------------------------------------------

# Edge ID -> InteractionEdge
self.interaction_edges: Dict[str, InteractionEdge] = {}

# Wallet -> Interaction IDs
self.interaction_index: Dict[str, Set[str]] = defaultdict(set)

# --------------------------------------------------------------------------
# Universal Edge Registry
# --------------------------------------------------------------------------

# Every edge regardless of type
self.edge_registry: Dict[
    str,
    Union[
        FundingEdge,
        DeploymentEdge,
        TransferEdge,
        BundleEdge,
        InteractionEdge,
    ],
] = {}

# --------------------------------------------------------------------------
# Graph Adjacency
# --------------------------------------------------------------------------

# Fast graph traversal
self.outgoing_edges: Dict[str, Set[str]] = defaultdict(set)
self.incoming_edges: Dict[str, Set[str]] = defaultdict(set)

# --------------------------------------------------------------------------
# Edge Lookup
# --------------------------------------------------------------------------

# (source, target) -> Edge IDs
self.edge_lookup: Dict[Tuple[str, str], Set[str]] = defaultdict(set)

# --------------------------------------------------------------------------
# Edge Counters
# --------------------------------------------------------------------------

self.total_funding_edges: int = 0
self.total_transfer_edges: int = 0
self.total_deployment_edges: int = 0
self.total_bundle_edges: int = 0
self.total_interaction_edges: int = 0

self.funding_outgoing[wallet]

self.transfer_incoming[wallet]

self.deployment_index[wallet]

self.bundle_index[wallet]

# Timestamp -> Edge IDs
self.edge_time_index: Dict[int, Set[str]] = defaultdict(set)

# ============================================================================
# Indexes
# ============================================================================

# --------------------------------------------------------------------------
# Wallet Index
# --------------------------------------------------------------------------

# Wallet Address -> WalletNode
self.wallet_index: Dict[str, WalletNode] = {}

# Wallet ID -> Wallet Address
self.wallet_id_index: Dict[int, str] = {}

# Wallet Label -> Wallet Addresses
self.wallet_label_index: Dict[str, Set[str]] = defaultdict(set)

# Wallet Role -> Wallet Addresses
self.wallet_role_index: Dict[WalletRole, Set[str]] = defaultdict(set)

# --------------------------------------------------------------------------
# Token Index
# --------------------------------------------------------------------------

# Token Mint -> TokenNode
self.token_index: Dict[str, TokenNode] = {}

# Symbol -> Token Mints
self.token_symbol_index: Dict[str, Set[str]] = defaultdict(set)

# Deployer Wallet -> Tokens
self.token_deployer_index: Dict[str, Set[str]] = defaultdict(set)

# --------------------------------------------------------------------------
# Source Index
# --------------------------------------------------------------------------

# Source Wallet -> Edge IDs
self.source_index: Dict[str, Set[str]] = defaultdict(set)

# --------------------------------------------------------------------------
# Destination Index
# --------------------------------------------------------------------------

# Destination Wallet -> Edge IDs
self.destination_index: Dict[str, Set[str]] = defaultdict(set)

# --------------------------------------------------------------------------
# Funding Index
# --------------------------------------------------------------------------

# Wallet -> Funding Edge IDs
self.funding_index: Dict[str, Set[str]] = defaultdict(set)

# Funding Wallet -> Funded Wallets
self.funder_index: Dict[str, Set[str]] = defaultdict(set)

# Funded Wallet -> Funding Wallets
self.funded_by_index: Dict[str, Set[str]] = defaultdict(set)

# --------------------------------------------------------------------------
# Deployment Index
# --------------------------------------------------------------------------

# Wallet -> Deployment Edge IDs
self.deployment_index: Dict[str, Set[str]] = defaultdict(set)

# Token -> Deployment Edge IDs
self.token_deployment_index: Dict[str, Set[str]] = defaultdict(set)

# --------------------------------------------------------------------------
# Cluster Index
# --------------------------------------------------------------------------

# Cluster ID -> Wallets
self.cluster_index: Dict[str, Set[str]] = defaultdict(set)

# Wallet -> Cluster ID
self.wallet_cluster_index: Dict[str, str] = {}

# Cluster -> Tokens
self.cluster_token_index: Dict[str, Set[str]] = defaultdict(set)

# --------------------------------------------------------------------------
# Reverse Lookup Indexes
# --------------------------------------------------------------------------

# Node ID -> Graph Index
self.node_graph_index: Dict[str, int] = {}

# Graph Index -> Node ID
self.reverse_graph_index: Dict[int, str] = {}

wallet = self.wallet_index[address]

tokens = self.token_deployer_index[address]

cluster = self.wallet_cluster_index[address]

funders = self.funded_by_index[address]

funded_wallets = self.funder_index[address]

deployments = self.deployment_index[address]

# Slot -> Edge IDs
self.slot_index: Dict[int, Set[str]] = defaultdict(set)

# Timestamp -> Edge IDs
self.timestamp_index: Dict[int, Set[str]] = defaultdict(set)

# Transaction Signature -> Edge ID
self.signature_index: Dict[str, str] = {}

# Program ID -> Edge IDs
self.program_index: Dict[str, Set[str]] = defaultdict(set)

# ============================================================================
# Caches
# ============================================================================

from cachetools import TTLCache

# --------------------------------------------------------------------------
# DFS Cache
# Key:
#     (start_node, max_depth)
#
# Value:
#     List[str]
# --------------------------------------------------------------------------

self.dfs_cache: TTLCache = TTLCache(
    maxsize=10_000,
    ttl=300,
)

# --------------------------------------------------------------------------
# BFS Cache
# Key:
#     (start_node, max_depth)
#
# Value:
#     List[str]
# --------------------------------------------------------------------------

self.bfs_cache: TTLCache = TTLCache(
    maxsize=10_000,
    ttl=300,
)

# --------------------------------------------------------------------------
# Shortest Path Cache
# Key:
#     (source, destination)
#
# Value:
#     List[str]
# --------------------------------------------------------------------------

self.shortest_path_cache: TTLCache = TTLCache(
    maxsize=20_000,
    ttl=600,
)

# --------------------------------------------------------------------------
# Funding Path Cache
# Key:
#     Wallet Address
#
# Value:
#     Funding Path
# --------------------------------------------------------------------------

self.funding_path_cache: TTLCache = TTLCache(
    maxsize=20_000,
    ttl=600,
)

# --------------------------------------------------------------------------
# Centrality Cache
# Key:
#     Wallet Address
#
# Value:
#     Centrality Score
# --------------------------------------------------------------------------

self.centrality_cache: TTLCache = TTLCache(
    maxsize=50_000,
    ttl=900,
)

# --------------------------------------------------------------------------
# Cluster Cache
# Key:
#     Wallet Address
#
# Value:
#     Cluster ID
# --------------------------------------------------------------------------

self.cluster_cache: TTLCache = TTLCache(
    maxsize=50_000,
    ttl=900,
)

# --------------------------------------------------------------------------
# Generic Query Cache
# --------------------------------------------------------------------------

self.query_cache: TTLCache = TTLCache(
    maxsize=100_000,
    ttl=120,
)

# --------------------------------------------------------------------------
# Cache Statistics
# --------------------------------------------------------------------------

self.cache_hits: int = 0
self.cache_misses: int = 0
self.cache_evictions: int = 0

# ============================================================================
# Statistics
# ============================================================================

from dataclasses import dataclass, field
from datetime import datetime
from time import perf_counter


@dataclass(slots=True)
class GraphStatistics:
    """
    Runtime statistics for DeployerGraph.
    """

    # ------------------------------------------------------------------
    # Graph Size
    # ------------------------------------------------------------------

    node_count: int = 0
    edge_count: int = 0

    wallet_count: int = 0
    token_count: int = 0

    funding_edge_count: int = 0
    deployment_edge_count: int = 0
    transfer_edge_count: int = 0
    bundle_edge_count: int = 0
    interaction_edge_count: int = 0

    cluster_count: int = 0

    # ------------------------------------------------------------------
    # Cache
    # ------------------------------------------------------------------

    cache_hits: int = 0
    cache_misses: int = 0
    cache_evictions: int = 0

    # ------------------------------------------------------------------
    # Build
    # ------------------------------------------------------------------

    build_started: datetime | None = None
    build_finished: datetime | None = None

    build_time: float = 0.0

    last_updated: datetime | None = None

    # ------------------------------------------------------------------
    # Runtime
    # ------------------------------------------------------------------

    dfs_calls: int = 0
    bfs_calls: int = 0
    shortest_path_calls: int = 0

    cluster_rebuilds: int = 0

    serialization_count: int = 0

    # ------------------------------------------------------------------
    # Memory
    # ------------------------------------------------------------------

    estimated_memory_mb: float = 0.0


# ============================================================================
# Inside DeployerGraph
# ============================================================================

self.statistics = GraphStatistics()

# Internal timer
self._build_timer = perf_counter()

self.statistics.build_started = datetime.utcnow()

start = perf_counter()

# build graph ...

self.statistics.build_finished = datetime.utcnow()

self.statistics.build_time = perf_counter() - start

self.statistics.cache_hits += 1

self.statistics.cache_misses += 1

self.statistics.cache_evictions += 1

self.statistics.wallet_count = len(self.wallet_nodes)

self.statistics.token_count = len(self.token_nodes)

self.statistics.node_count = (
    self.statistics.wallet_count
    + self.statistics.token_count
)

self.statistics.edge_count = (
    self.statistics.funding_edge_count
    + self.statistics.transfer_edge_count
    + self.statistics.deployment_edge_count
    + self.statistics.bundle_edge_count
    + self.statistics.interaction_edge_count
)

# ============================================================================
# Synchronization
# ============================================================================

import asyncio
from contextlib import asynccontextmanager

# --------------------------------------------------------------------------
# Async Lock
# General async operations
# --------------------------------------------------------------------------

self.async_lock = asyncio.Lock()

# --------------------------------------------------------------------------
# Graph Lock
# Protects graph mutations
# --------------------------------------------------------------------------

self.graph_lock = asyncio.Lock()

# --------------------------------------------------------------------------
# Cache Lock
# Protects cache updates
# --------------------------------------------------------------------------

self.cache_lock = asyncio.Lock()

# --------------------------------------------------------------------------
# Index Lock
# Protects index updates
# --------------------------------------------------------------------------

self.index_lock = asyncio.Lock()

# --------------------------------------------------------------------------
# Build Lock
# Prevents concurrent graph builds
# --------------------------------------------------------------------------

self.build_lock = asyncio.Lock()

# --------------------------------------------------------------------------
# Statistics Lock
# --------------------------------------------------------------------------

self.statistics_lock = asyncio.Lock()

# --------------------------------------------------------------------------
# Serialization Lock
# --------------------------------------------------------------------------

self.serialization_lock = asyncio.Lock()

# --------------------------------------------------------------------------
# Shutdown Event
# --------------------------------------------------------------------------

self.shutdown_event = asyncio.Event()

# ============================================================================
# Lock Helpers
# ============================================================================

@asynccontextmanager
async def graph_context(self):

    async with self.graph_lock:
        yield


@asynccontextmanager
async def cache_context(self):

    async with self.cache_lock:
        yield


@asynccontextmanager
async def index_context(self):

    async with self.index_lock:
        yield


@asynccontextmanager
async def build_context(self):

    async with self.build_lock:
        yield

async with self.graph_context():

    self.graph.add_node(...)

async with self.index_context():

    self.wallet_index[address] = wallet

async with self.cache_context():

    self.dfs_cache[key] = result

# ============================================================================
# Workers
# ============================================================================

import asyncio

from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor

# --------------------------------------------------------------------------
# Thread Pool
# I/O-bound work
# --------------------------------------------------------------------------

self.thread_pool = ThreadPoolExecutor(
    max_workers=self.config.thread_workers,
    thread_name_prefix="DeployerGraphThread",
)

# --------------------------------------------------------------------------
# Process Pool
# CPU-bound graph algorithms
# --------------------------------------------------------------------------

self.process_pool = ProcessPoolExecutor(
    max_workers=self.config.process_workers,
)

# --------------------------------------------------------------------------
# Async Queue
# --------------------------------------------------------------------------

self.work_queue: asyncio.Queue = asyncio.Queue(
    maxsize=self.config.queue_size,
)

# Priority Queue

self.priority_queue: asyncio.PriorityQueue = asyncio.PriorityQueue(
    maxsize=self.config.priority_queue_size,
)

# --------------------------------------------------------------------------
# Worker Tasks
# --------------------------------------------------------------------------

self.background_tasks: set[asyncio.Task] = set()

self.worker_tasks: list[asyncio.Task] = []

# --------------------------------------------------------------------------
# Worker State
# --------------------------------------------------------------------------

self.workers_running: bool = False

self.active_jobs: int = 0

self.completed_jobs: int = 0

self.failed_jobs: int = 0

# --------------------------------------------------------------------------
# Semaphore
# Limits concurrent jobs
# --------------------------------------------------------------------------

self.worker_semaphore = asyncio.Semaphore(
    self.config.max_concurrent_jobs
)

from enum import Enum


class WorkerJob(Enum):

    BUILD_GRAPH = "build_graph"

    UPDATE_GRAPH = "update_graph"

    CALCULATE_CENTRALITY = "calculate_centrality"

    FIND_CLUSTER = "find_cluster"

    FIND_FUNDING_PATH = "find_funding_path"

    DFS = "dfs"

    BFS = "bfs"

    SERIALIZE = "serialize"

    SAVE_DATABASE = "save_database"


self.background_task_registry = {

    WorkerJob.BUILD_GRAPH: None,

    WorkerJob.UPDATE_GRAPH: None,

    WorkerJob.CALCULATE_CENTRALITY: None,

    WorkerJob.FIND_CLUSTER: None,

    WorkerJob.FIND_FUNDING_PATH: None,

}

# ============================================================================
# Configuration
# ============================================================================

from dataclasses import dataclass, field
from pathlib import Path
import logging


# ----------------------------------------------------------------------------
# Graph Configuration
# ----------------------------------------------------------------------------

@dataclass(slots=True)
class GraphConfig:

    backend: str = "rustworkx"

    directed: bool = True

    max_graph_depth: int = 25

    max_cluster_size: int = 10000

    max_related_wallets: int = 5000

    max_edges_per_wallet: int = 50000

    enable_centrality: bool = True

    enable_clustering: bool = True

    enable_funding_trace: bool = True

    auto_rebuild: bool = False


# ----------------------------------------------------------------------------
# Cache Configuration
# ----------------------------------------------------------------------------

@dataclass(slots=True)
class CacheConfig:

    dfs_cache_size: int = 10000

    bfs_cache_size: int = 10000

    shortest_path_cache_size: int = 20000

    funding_cache_size: int = 20000

    cluster_cache_size: int = 50000

    centrality_cache_size: int = 50000

    cache_ttl_seconds: int = 600


# ----------------------------------------------------------------------------
# Worker Configuration
# ----------------------------------------------------------------------------

@dataclass(slots=True)
class WorkerConfig:

    thread_workers: int = 8

    process_workers: int = 4

    queue_size: int = 10000

    priority_queue_size: int = 5000

    max_concurrent_jobs: int = 16


# ----------------------------------------------------------------------------
# Main Configuration
# ----------------------------------------------------------------------------

@dataclass(slots=True)
class DeployerGraphConfig:

    graph: GraphConfig = field(default_factory=GraphConfig)

    cache: CacheConfig = field(default_factory=CacheConfig)

    workers: WorkerConfig = field(default_factory=WorkerConfig)

    log_level: int = logging.INFO

    log_directory: Path = Path("logs")

@dataclass(slots=True)
class GraphDependencies:

    wallet_db: WalletDatabase

    token_db: TokenDatabase

    cache: CacheManager

    transaction_fetcher: TransactionFetcher   

# ============================================================================
# Logger
# ============================================================================

self.logger = logging.getLogger("SentinelAI.DeployerGraph")

self.logger.setLevel(self.config.log_level)

# ============================================================================
# Database References
# ============================================================================

self.wallet_db: WalletDatabase = wallet_database

self.token_db: TokenDatabase = token_database

self.cache_manager: CacheManager = cache_manager

self.transaction_fetcher: TransactionFetcher = transaction_fetcher

self.config = DeployerGraphConfig()

self.graph_config = self.config.graph

self.cache_config = self.config.cache

self.worker_config = self.config.workers

def __init__(
    self,
    dependencies: GraphDependencies,
    config: DeployerGraphConfig,
):
    self.dependencies = dependencies
    self.config = config