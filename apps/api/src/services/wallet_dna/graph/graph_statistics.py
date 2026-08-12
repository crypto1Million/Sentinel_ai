"""
graph_statistics.py

Production Graph Statistics Engine

Responsible for:

• Graph analytics
• Centrality analytics
• Degree analytics
• Cluster analytics
• Funding analytics
• Deployer analytics
• Performance metrics
"""

from __future__ import annotations

# =============================================================================
# Standard Library
# =============================================================================

import copy
import json
import logging
import math
import statistics
import sys
import time

from collections import (
    Counter,
    defaultdict,
)

from dataclasses import (
    asdict,
    dataclass,
    field,
)

from datetime import (
    datetime,
    timedelta,
    timezone,
)

from enum import (
    Enum,
    IntEnum,
)

from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    Iterator,
    List,
    Optional,
    Sequence,
    Set,
    Tuple,
    Union,
)

# =============================================================================
# Third Party
# =============================================================================

import networkx as nx
import numpy as np

try:
    import rustworkx as rx
except ImportError:
    rx = None

# =============================================================================
# Internal Modules
# =============================================================================

from .deployer_models import (
    WalletNode,
    TokenNode,
    FundingEdge,
    DeploymentEdge,
    TransferEdge,
    BundleEdge,
    InteractionEdge,
)

from .deployer_graph import DeployerGraph
from .graph_storage import GraphStorage
from .graph_indexes import GraphIndexes
from .graph_cache import GraphCache

# =============================================================================
# Logger
# =============================================================================

logger = logging.getLogger(__name__)

# =============================================================================
# Constants
# =============================================================================

# ---------------------------------------------------------------------------
# Graph Version
# ---------------------------------------------------------------------------

GRAPH_STATISTICS_VERSION = "1.0.0"

# ---------------------------------------------------------------------------
# Default Configuration
# ---------------------------------------------------------------------------

DEFAULT_LOOKBACK_DAYS = 365

DEFAULT_TOP_N = 100

DEFAULT_CLUSTER_LIMIT = 500

DEFAULT_BATCH_SIZE = 1000

DEFAULT_TIMEOUT = 30

# ---------------------------------------------------------------------------
# Graph Limits
# ---------------------------------------------------------------------------

MAX_GRAPH_DEPTH = 20

MAX_FUNDING_DEPTH = 10

MAX_CLUSTER_SIZE = 100000

MAX_NODE_COUNT = 10_000_000

MAX_EDGE_COUNT = 100_000_000

# ---------------------------------------------------------------------------
# Centrality Configuration
# ---------------------------------------------------------------------------

ENABLE_PAGERANK = True

ENABLE_EIGENVECTOR = True

ENABLE_BETWEENNESS = True

ENABLE_CLOSENESS = True

ENABLE_DEGREE_CENTRALITY = True

CENTRALITY_MAX_ITERATIONS = 100

CENTRALITY_TOLERANCE = 1e-6

# ---------------------------------------------------------------------------
# Degree Statistics
# ---------------------------------------------------------------------------

MIN_DEGREE = 0

MAX_DEGREE = 1_000_000

DEGREE_BUCKET_SIZE = 5

# ---------------------------------------------------------------------------
# Cluster Analysis
# ---------------------------------------------------------------------------

MIN_CLUSTER_SIZE = 2

LARGE_CLUSTER_THRESHOLD = 50

MEGA_CLUSTER_THRESHOLD = 500

# ---------------------------------------------------------------------------
# Funding Analysis
# ---------------------------------------------------------------------------

MIN_FUNDING_AMOUNT = 0.01

HIGH_VALUE_TRANSFER = 100

FUNDING_DECIMAL_PRECISION = 6

# ---------------------------------------------------------------------------
# Deployer Statistics
# ---------------------------------------------------------------------------

MIN_DEPLOYMENTS_FOR_REPUTATION = 3

SUCCESS_RATE_THRESHOLD = 0.70

RUG_RATE_THRESHOLD = 0.30

# ---------------------------------------------------------------------------
# Performance
# ---------------------------------------------------------------------------

MEMORY_WARNING_MB = 2048

MEMORY_CRITICAL_MB = 4096

PERFORMANCE_SAMPLE_SIZE = 100

# ---------------------------------------------------------------------------
# Export
# ---------------------------------------------------------------------------

EXPORT_JSON_INDENT = 4

EXPORT_ENCODING = "utf-8"

# ---------------------------------------------------------------------------
# Floating Point
# ---------------------------------------------------------------------------

FLOAT_PRECISION = 6

EPSILON = 1e-9

# ---------------------------------------------------------------------------
# Unknown Values
# ---------------------------------------------------------------------------

UNKNOWN_CLUSTER = "UNKNOWN_CLUSTER"

UNKNOWN_DEPLOYER = "UNKNOWN_DEPLOYER"

UNKNOWN_TOKEN = "UNKNOWN_TOKEN"

UNKNOWN_WALLET = "UNKNOWN_WALLET"

# ---------------------------------------------------------------------------
# Report Sections
# ---------------------------------------------------------------------------

REPORT_GRAPH = "graph"

REPORT_CLUSTER = "cluster"

REPORT_FUNDING = "funding"

REPORT_DEPLOYER = "deployer"

REPORT_PERFORMANCE = "performance"

REPORT_CENTRALITY = "centrality"

# =============================================================================
# Enums
# =============================================================================

from enum import Enum, IntEnum, auto


# -----------------------------------------------------------------------------
# Graph Analysis State
# -----------------------------------------------------------------------------

class GraphState(Enum):
    """
    Current lifecycle state of the graph.
    """

    UNINITIALIZED = "uninitialized"
    INITIALIZING = "initializing"
    BUILDING = "building"
    READY = "ready"
    UPDATING = "updating"
    ANALYZING = "analyzing"
    FAILED = "failed"
    CLOSED = "closed"


# -----------------------------------------------------------------------------
# Node Types
# -----------------------------------------------------------------------------

class NodeType(Enum):
    """
    Types of nodes inside WalletDNA graph.
    """

    WALLET = "wallet"
    TOKEN = "token"
    DEPLOYER = "deployer"
    BUNDLE = "bundle"
    CONTRACT = "contract"
    PROGRAM = "program"
    UNKNOWN = "unknown"


# -----------------------------------------------------------------------------
# Edge Types
# -----------------------------------------------------------------------------

class EdgeType(Enum):
    """
    Graph edge categories.
    """

    FUNDING = "funding"
    DEPLOYMENT = "deployment"
    TRANSFER = "transfer"
    BUNDLE = "bundle"
    INTERACTION = "interaction"
    OWNERSHIP = "ownership"
    CREATION = "creation"


# -----------------------------------------------------------------------------
# Degree Type
# -----------------------------------------------------------------------------

class DegreeType(Enum):

    IN = "in"

    OUT = "out"

    TOTAL = "total"


# -----------------------------------------------------------------------------
# Centrality Algorithms
# -----------------------------------------------------------------------------

class CentralityAlgorithm(Enum):

    DEGREE = "degree"

    BETWEENNESS = "betweenness"

    CLOSENESS = "closeness"

    EIGENVECTOR = "eigenvector"

    PAGERANK = "pagerank"


# -----------------------------------------------------------------------------
# Cluster Type
# -----------------------------------------------------------------------------

class ClusterType(Enum):

    ISOLATED = "isolated"

    SMALL = "small"

    MEDIUM = "medium"

    LARGE = "large"

    MEGA = "mega"


# -----------------------------------------------------------------------------
# Funding Source
# -----------------------------------------------------------------------------

class FundingSource(Enum):

    UNKNOWN = "unknown"

    CEX = "cex"

    DEX = "dex"

    BRIDGE = "bridge"

    DEPLOYER = "deployer"

    TEAM = "team"

    INVESTOR = "investor"

    AIRDROP = "airdrop"

    MIXER = "mixer"


# -----------------------------------------------------------------------------
# Reputation Level
# -----------------------------------------------------------------------------

class ReputationLevel(Enum):

    UNKNOWN = "unknown"

    VERY_LOW = "very_low"

    LOW = "low"

    MEDIUM = "medium"

    HIGH = "high"

    VERY_HIGH = "very_high"

    ELITE = "elite"


# -----------------------------------------------------------------------------
# Launch Status
# -----------------------------------------------------------------------------

class LaunchStatus(Enum):

    UNKNOWN = "unknown"

    ACTIVE = "active"

    DEAD = "dead"

    RUGGED = "rugged"

    SUCCESSFUL = "successful"

    MIGRATED = "migrated"


# -----------------------------------------------------------------------------
# Statistics Mode
# -----------------------------------------------------------------------------

class StatisticsMode(Enum):

    QUICK = "quick"

    STANDARD = "standard"

    FULL = "full"

    DEEP = "deep"


# -----------------------------------------------------------------------------
# Performance Level
# -----------------------------------------------------------------------------

class PerformanceLevel(IntEnum):

    VERY_SLOW = 1

    SLOW = 2

    NORMAL = 3

    FAST = 4

    VERY_FAST = 5


# -----------------------------------------------------------------------------
# Report Type
# -----------------------------------------------------------------------------

class ReportType(Enum):

    SUMMARY = "summary"

    GRAPH = "graph"

    FUNDING = "funding"

    CLUSTER = "cluster"

    CENTRALITY = "centrality"

    DEPLOYER = "deployer"

    PERFORMANCE = "performance"

    FULL = "full"


# -----------------------------------------------------------------------------
# Export Format
# -----------------------------------------------------------------------------

class ExportFormat(Enum):

    JSON = "json"

    CSV = "csv"

    YAML = "yaml"

    PARQUET = "parquet"


# =============================================================================
# Statistics Models
# =============================================================================

from dataclasses import dataclass, field
from typing import Dict, List, Optional


# =============================================================================
# Graph Metrics
# =============================================================================

@dataclass(slots=True)
class GraphMetrics:
    """
    Core graph metrics.

    Computed frequently and cached.
    """

    total_nodes: int = 0

    total_edges: int = 0

    total_wallets: int = 0

    total_tokens: int = 0

    total_funding_edges: int = 0

    total_transfer_edges: int = 0

    total_deployment_edges: int = 0

    total_bundle_edges: int = 0

    total_interaction_edges: int = 0

    density: float = 0.0

    average_degree: float = 0.0

    connected_components: int = 0

    largest_component_size: int = 0

    isolated_nodes: int = 0

    graph_depth: int = 0

    created_at: float = 0.0

    updated_at: float = 0.0


# =============================================================================
# Degree Statistics
# =============================================================================

@dataclass(slots=True)
class DegreeStatistics:
    """
    Degree analysis.
    """

    average_degree: float = 0.0

    median_degree: float = 0.0

    maximum_degree: int = 0

    minimum_degree: int = 0

    average_in_degree: float = 0.0

    average_out_degree: float = 0.0

    max_in_degree: int = 0

    max_out_degree: int = 0

    degree_variance: float = 0.0

    degree_std: float = 0.0

    degree_distribution: Dict[int, int] = field(
        default_factory=dict
    )

    top_degree_wallets: List[str] = field(
        default_factory=list
    )


# =============================================================================
# Centrality Statistics
# =============================================================================

@dataclass(slots=True)
class CentralityStatistics:
    """
    Centrality analytics.

    Every dictionary maps:

        wallet -> score
    """

    degree: Dict[str, float] = field(
        default_factory=dict
    )

    betweenness: Dict[str, float] = field(
        default_factory=dict
    )

    closeness: Dict[str, float] = field(
        default_factory=dict
    )

    eigenvector: Dict[str, float] = field(
        default_factory=dict
    )

    pagerank: Dict[str, float] = field(
        default_factory=dict
    )

    top_degree_wallets: List[str] = field(
        default_factory=list
    )

    top_betweenness_wallets: List[str] = field(
        default_factory=list
    )

    top_closeness_wallets: List[str] = field(
        default_factory=list
    )

    top_eigenvector_wallets: List[str] = field(
        default_factory=list
    )

    top_pagerank_wallets: List[str] = field(
        default_factory=list
    )

    calculated_at: float = 0.0

    algorithm_runtime: float = 0.0


# =============================================================================
# Cluster Statistics
# =============================================================================

@dataclass(slots=True)
class ClusterStatistics:
    """
    Connected-component / wallet-cluster statistics.
    """

    total_clusters: int = 0

    isolated_clusters: int = 0

    small_clusters: int = 0

    medium_clusters: int = 0

    large_clusters: int = 0

    mega_clusters: int = 0

    largest_cluster_size: int = 0

    average_cluster_size: float = 0.0

    median_cluster_size: float = 0.0

    cluster_variance: float = 0.0

    cluster_std: float = 0.0

    isolated_wallets: int = 0

    clustered_wallets: int = 0

    cluster_distribution: Dict[int, int] = field(
        default_factory=dict
    )

    largest_clusters: List[str] = field(
        default_factory=list
    )

    cluster_sizes: Dict[str, int] = field(
        default_factory=dict
    )

    cluster_density: Dict[str, float] = field(
        default_factory=dict
    )

    calculated_at: float = 0.0

    runtime: float = 0.0


# =============================================================================
# Funding Statistics
# =============================================================================

@dataclass(slots=True)
class FundingStatistics:
    """
    Funding graph statistics.
    """

    total_funding_edges: int = 0

    total_funding_paths: int = 0

    average_funding_depth: float = 0.0

    maximum_funding_depth: int = 0

    minimum_funding_depth: int = 0

    average_path_length: float = 0.0

    average_transfer_amount: float = 0.0

    total_transferred_sol: float = 0.0

    total_transferred_usd: float = 0.0

    unique_funders: int = 0

    unique_receivers: int = 0

    bridge_wallets: int = 0

    cex_wallets: int = 0

    dex_wallets: int = 0

    funding_tree_size: int = 0

    funding_sources: Counter = field(
        default_factory=Counter
    )

    funding_destinations: Counter = field(
        default_factory=Counter
    )

    funding_depth_distribution: Dict[int, int] = field(
        default_factory=dict
    )

    top_funders: List[str] = field(
        default_factory=list
    )

    top_receivers: List[str] = field(
        default_factory=list
    )

    calculated_at: float = 0.0

    runtime: float = 0.0


# =============================================================================
# Deployer Statistics
# =============================================================================

@dataclass(slots=True)
class DeployerStatistics:
    """
    Deployer analytics.
    """

    total_deployers: int = 0

    active_deployers: int = 0

    inactive_deployers: int = 0

    successful_deployers: int = 0

    rugged_deployers: int = 0

    suspicious_deployers: int = 0

    average_launches: float = 0.0

    median_launches: float = 0.0

    maximum_launches: int = 0

    minimum_launches: int = 0

    successful_launches: int = 0

    failed_launches: int = 0

    rugged_launches: int = 0

    migrated_launches: int = 0

    rug_rate: float = 0.0

    success_rate: float = 0.0

    average_token_lifetime: float = 0.0

    reputation_distribution: Dict[
        ReputationLevel,
        int,
    ] = field(
        default_factory=dict
    )

    deployer_launch_count: Dict[
        str,
        int,
    ] = field(
        default_factory=dict
    )

    deployer_success_rate: Dict[
        str,
        float,
    ] = field(
        default_factory=dict
    )

    top_deployers: List[str] = field(
        default_factory=list
    )

    elite_deployers: List[str] = field(
        default_factory=list
    )

    blacklist: Set[str] = field(
        default_factory=set
    )

    whitelist: Set[str] = field(
        default_factory=set
    )

    calculated_at: float = 0.0

    runtime: float = 0.0

# =============================================================================
# Performance Statistics
# =============================================================================

@dataclass(slots=True)
class PerformanceStatistics:
    """
    Runtime performance metrics for WalletDNA graph.
    """

    build_time: float = 0.0

    traversal_time: float = 0.0

    shortest_path_time: float = 0.0

    funding_analysis_time: float = 0.0

    cluster_detection_time: float = 0.0

    centrality_time: float = 0.0

    deployer_analysis_time: float = 0.0

    serialization_time: float = 0.0

    deserialization_time: float = 0.0

    average_query_time: float = 0.0

    fastest_query: float = 0.0

    slowest_query: float = 0.0

    average_batch_time: float = 0.0

    total_queries: int = 0

    total_traversals: int = 0

    total_updates: int = 0

    graph_memory_mb: float = 0.0

    graph_disk_mb: float = 0.0

    node_memory_mb: float = 0.0

    edge_memory_mb: float = 0.0

    throughput_nodes_per_second: float = 0.0

    throughput_edges_per_second: float = 0.0

    cpu_usage: float = 0.0

    ram_usage: float = 0.0

    peak_ram_usage: float = 0.0

    uptime: float = 0.0

    calculated_at: float = 0.0


# =============================================================================
# Cache Statistics
# =============================================================================

@dataclass(slots=True)
class CacheStatistics:
    """
    Statistics collected from GraphCache.
    """

    cache_hits: int = 0

    cache_misses: int = 0

    cache_puts: int = 0

    cache_removals: int = 0

    cache_invalidations: int = 0

    cleanup_runs: int = 0

    hit_rate: float = 0.0

    miss_rate: float = 0.0

    dfs_cache_size: int = 0

    bfs_cache_size: int = 0

    shortest_path_cache_size: int = 0

    funding_cache_size: int = 0

    centrality_cache_size: int = 0

    cluster_cache_size: int = 0

    total_cache_entries: int = 0

    cache_memory_mb: float = 0.0

    cache_disk_mb: float = 0.0

    average_entry_size_bytes: float = 0.0

    maximum_entry_size_bytes: int = 0

    oldest_entry_age: float = 0.0

    newest_entry_age: float = 0.0

    expired_entries: int = 0

    evicted_entries: int = 0

    cache_efficiency: float = 0.0

    calculated_at: float = 0.0

# =============================================================================
# Graph Summary
# =============================================================================

@dataclass(slots=True)
class GraphSummary:
    """
    High-level summary of the graph.

    Used by:
        • Dashboard
        • Sentinel Score
        • API responses
    """

    graph_version: str = GRAPH_STATISTICS_VERSION

    created_at: float = 0.0

    updated_at: float = 0.0

    graph_state: GraphState = GraphState.READY

    metrics: GraphMetrics = field(
        default_factory=GraphMetrics
    )

    degree: DegreeStatistics = field(
        default_factory=DegreeStatistics
    )

    centrality: CentralityStatistics = field(
        default_factory=CentralityStatistics
    )

    cluster: ClusterStatistics = field(
        default_factory=ClusterStatistics
    )

    funding: FundingStatistics = field(
        default_factory=FundingStatistics
    )

    deployer: DeployerStatistics = field(
        default_factory=DeployerStatistics
    )

    performance: PerformanceStatistics = field(
        default_factory=PerformanceStatistics
    )

    cache: CacheStatistics = field(
        default_factory=CacheStatistics
    )


# =============================================================================
# Graph Report
# =============================================================================

@dataclass(slots=True)
class GraphReport:
    """
    Complete analysis report.

    Can be exported as:

        JSON
        CSV
        Dashboard
        API
    """

    report_id: str = ""

    report_name: str = "WalletDNA Report"

    report_type: ReportType = ReportType.FULL

    export_format: ExportFormat = ExportFormat.JSON

    generated_at: float = 0.0

    generated_by: str = "SentinelAI"

    graph_summary: GraphSummary = field(
        default_factory=GraphSummary
    )

    notes: List[str] = field(
        default_factory=list
    )

    warnings: List[str] = field(
        default_factory=list
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )


# =============================================================================
# Statistics Snapshot
# =============================================================================

@dataclass(slots=True)
class StatisticsSnapshot:
    """
    Snapshot of graph statistics.

    Used for:

        • History
        • Restore
        • Time-series
    """

    timestamp: float = 0.0

    graph_state: GraphState = GraphState.READY

    summary: GraphSummary = field(
        default_factory=GraphSummary
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )


# =============================================================================
# Statistics Export
# =============================================================================

@dataclass(slots=True)
class StatisticsExport:
  
    Serializable export model.
   

    version: str = GRAPH_STATISTICS_VERSION

    export_format: ExportFormat = ExportFormat.JSON

    exported_at: float = 0.0

    report: GraphReport = field(
        default_factory=GraphReport
    )

    checksum: str = ""

    compressed: bool = False

    encrypted: bool = False

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

# =============================================================================
# Graph Statistics Engine
# =============================================================================


class GraphStatistics:

    Production statistics engine for WalletDNA.

    Responsibilities
    ----------------
    • Graph metrics
    • Degree analysis
    • Centrality analysis
    • Cluster analysis
    • Funding analysis
    • Deployer analysis
    • Performance monitoring
    • Cache statistics
    • Report generation
  

    ###########################################################################
    # Constructor
    ###########################################################################

    def __init__(
        self,
        graph: Optional["DeployerGraph"] = None,
        storage: Optional["GraphStorage"] = None,
        indexes: Optional["GraphIndexes"] = None,
        cache: Optional["GraphCache"] = None,
    ) -> None:

        self.graph = graph

        self.storage = storage

        self.indexes = indexes

        self.cache = cache

        self.logger = logger

        self._initialize_configuration()

        self._initialize_metrics()

        self._initialize_counters()

    ###########################################################################
    # Initialization
    ###########################################################################

    def _initialize_configuration(self) -> None:
        ...

    def _initialize_metrics(self) -> None:
        ...

    def _initialize_counters(self) -> None:
        ...

    ###########################################################################
    # Graph Statistics
    ###########################################################################

    def total_nodes(self):
        ...

    def total_edges(self):
        ...

    def wallet_count(self):
        ...

    def token_count(self):
        ...

    def funding_edge_count(self):
        ...

    def deployment_edge_count(self):
        ...

    def transfer_edge_count(self):
        ...

    def bundle_edge_count(self):
        ...

    def interaction_edge_count(self):
        ...

    ###########################################################################
    # Degree Statistics
    ###########################################################################

    def average_degree(self):
        ...

    def max_degree(self):
        ...

    def min_degree(self):
        ...

    def in_degree(self):
        ...

    def out_degree(self):
        ...

    def degree_distribution(self):
        ...

    ###########################################################################
    # Centrality Statistics
    ###########################################################################

    def degree_centrality(self):
        ...

    def betweenness_centrality(self):
        ...

    def closeness_centrality(self):
        ...

    def eigenvector_centrality(self):
        ...

    def pagerank(self):
        ...

    def top_central_wallets(self):
        ...

    ###########################################################################
    # Cluster Statistics
    ###########################################################################

    def cluster_count(self):
        ...

    def largest_cluster(self):
        ...

    def average_cluster_size(self):
        ...

    def isolated_wallets(self):
        ...

    def cluster_distribution(self):
        ...

    ###########################################################################
    # Funding Statistics
    ###########################################################################

    def average_funding_depth(self):
        ...

    def maximum_funding_depth(self):
        ...

    def funding_sources(self):
        ...

    def funding_destinations(self):
        ...

    def funding_tree_size(self):
        ...

    ###########################################################################
    # Deployer Statistics
    ###########################################################################

    def deployer_count(self):
        ...

    def average_launches(self):
        ...

    def successful_launches(self):
        ...

    def rug_rate(self):
        ...

    def reputation_distribution(self):
        ...

    ###########################################################################
    # Performance Statistics
    ###########################################################################

    def graph_memory(self):
        ...

    def cache_memory(self):
        ...

    def build_time(self):
        ...

    def traversal_time(self):
        ...

    def cache_hit_rate(self):
        ...

    def throughput(self):
        ...

    ###########################################################################
    # Reports
    ###########################################################################

    def summary(self):
        ...

    def graph_report(self):
        ...

    def funding_report(self):
        ...

    def deployer_report(self):
        ...

    def export_statistics(self):
        ...

    ###########################################################################
    # Utilities
    ###########################################################################

    def reset(self):
        ...

    def snapshot(self):
        ...

    def restore(self):
        ...

    def pretty_print(self):
        ...

###############################################################################
# Constructor
###############################################################################

def __init__(
    self,
    graph: Optional["DeployerGraph"] = None,
    storage: Optional["GraphStorage"] = None,
    indexes: Optional["GraphIndexes"] = None,
    cache: Optional["GraphCache"] = None,
) -> None:
  
    Initialize Graph Statistics Engine.

    Parameters
    ----------
    graph
        Active graph engine.

    storage
        GraphStorage instance.

    indexes
        GraphIndexes instance.

    cache
        GraphCache instance.
  

    ###########################################################################
    # Core References
    ###########################################################################

    self.graph = graph

    self.storage = storage

    self.indexes = indexes

    self.cache = cache

    ###########################################################################
    # Logger
    ###########################################################################

    self.logger = logger

    ###########################################################################
    # Metadata
    ###########################################################################

    self.version = GRAPH_STATISTICS_VERSION

    self.created_at = time.time()

    self.last_updated = self.created_at

    self.last_analysis = 0.0

    ###########################################################################
    # Configuration
    ###########################################################################

    self.configuration: Dict[str, Any] = {}

    ###########################################################################
    # Models
    ###########################################################################

    self.metrics = GraphMetrics()

    self.degree_statistics = DegreeStatistics()

    self.centrality_statistics = CentralityStatistics()

    self.cluster_statistics = ClusterStatistics()

    self.funding_statistics = FundingStatistics()

    self.deployer_statistics = DeployerStatistics()

    self.performance_statistics = PerformanceStatistics()

    self.cache_statistics = CacheStatistics()

    self.graph_summary = GraphSummary()

    ###########################################################################
    # Runtime Flags
    ###########################################################################

    self.initialized = False

    self.statistics_ready = False

    self.centrality_ready = False

    self.cluster_ready = False

    self.performance_ready = False

    ###########################################################################
    # Runtime State
    ###########################################################################

    self.graph_state = GraphState.UNINITIALIZED

    self.analysis_mode = StatisticsMode.STANDARD

    ###########################################################################
    # Internal Metrics
    ###########################################################################

    self._initialize_metrics()

    ###########################################################################
    # Internal Counters
    ###########################################################################

    self._initialize_counters()

    ###########################################################################
    # Configuration
    ###########################################################################

    self._initialize_configuration()

    ###########################################################################
    # Finish
    ###########################################################################

    self.initialized = True

    self.graph_state = GraphState.READY

    self.logger.info(
        "GraphStatistics initialized successfully."
    )


###############################################################################
# Metric Initialization
###############################################################################

def _initialize_metrics(self) -> None:
    """
    Initialize every statistics model.

    Called exactly once during GraphStatistics construction.

    Creates fresh metric containers for all graph analytics.
    """

    self.logger.debug("Initializing graph metrics...")

    ###########################################################################
    # Core Metrics
    ###########################################################################

    self.metrics = GraphMetrics()

    ###########################################################################
    # Degree Statistics
    ###########################################################################

    self.degree_statistics = DegreeStatistics()

    ###########################################################################
    # Centrality Statistics
    ###########################################################################

    self.centrality_statistics = CentralityStatistics()

    ###########################################################################
    # Cluster Statistics
    ###########################################################################

    self.cluster_statistics = ClusterStatistics()

    ###########################################################################
    # Funding Statistics
    ###########################################################################

    self.funding_statistics = FundingStatistics()

    ###########################################################################
    # Deployer Statistics
    ###########################################################################

    self.deployer_statistics = DeployerStatistics()

    ###########################################################################
    # Performance Statistics
    ###########################################################################

    self.performance_statistics = PerformanceStatistics()

    ###########################################################################
    # Cache Statistics
    ###########################################################################

    self.cache_statistics = CacheStatistics()

    ###########################################################################
    # Graph Summary
    ###########################################################################

    self.graph_summary = GraphSummary()

    ###########################################################################
    # Runtime Reports
    ###########################################################################

    self.graph_report = GraphReport()

    self.statistics_snapshot = StatisticsSnapshot()

    self.statistics_export = StatisticsExport()

    ###########################################################################
    # Runtime Analysis Results
    ###########################################################################

    self.latest_summary: Optional[GraphSummary] = None

    self.latest_report: Optional[GraphReport] = None

    self.latest_snapshot: Optional[StatisticsSnapshot] = None

    self.latest_export: Optional[StatisticsExport] = None

    ###########################################################################
    # Runtime Flags
    ###########################################################################

    self.metrics_initialized = True

    self.logger.info("Graph statistics metrics initialized successfully.")

###############################################################################
# Counter Initialization
###############################################################################

def _initialize_counters(self) -> None:
    """
    Initialize all runtime counters.

    These counters track graph usage, performance,
    analytics execution, cache activity,
    and engine health.
    """

    self.logger.debug("Initializing statistics counters...")

    ###########################################################################
    # Graph Counters
    ###########################################################################

    self.node_count = 0
    self.edge_count = 0

    self.wallet_count_counter = 0
    self.token_count_counter = 0

    self.funding_edge_counter = 0
    self.deployment_edge_counter = 0
    self.transfer_edge_counter = 0
    self.bundle_edge_counter = 0
    self.interaction_edge_counter = 0

    ###########################################################################
    # Analysis Counters
    ###########################################################################

    self.total_analyses = 0

    self.graph_analysis_runs = 0
    self.centrality_runs = 0
    self.cluster_runs = 0
    self.funding_runs = 0
    self.deployer_runs = 0

    ###########################################################################
    # Query Counters
    ###########################################################################

    self.total_queries = 0

    self.wallet_queries = 0
    self.token_queries = 0

    self.cluster_queries = 0
    self.path_queries = 0

    self.statistics_queries = 0

    ###########################################################################
    # Traversal Counters
    ###########################################################################

    self.total_traversals = 0

    self.dfs_runs = 0
    self.bfs_runs = 0

    self.shortest_path_runs = 0

    ###########################################################################
    # Cache Counters
    ###########################################################################

    self.cache_hits = 0
    self.cache_misses = 0

    self.cache_puts = 0
    self.cache_removals = 0

    self.cache_invalidations = 0

    ###########################################################################
    # Update Counters
    ###########################################################################

    self.total_updates = 0

    self.wallet_updates = 0
    self.token_updates = 0

    self.graph_rebuilds = 0

    ###########################################################################
    # Export Counters
    ###########################################################################

    self.exports_created = 0

    self.snapshots_created = 0
    self.snapshots_restored = 0

    ###########################################################################
    # Performance Counters
    ###########################################################################

    self.total_runtime = 0.0

    self.total_build_time = 0.0

    self.total_traversal_time = 0.0

    self.total_query_time = 0.0

    self.total_analysis_time = 0.0

    ###########################################################################
    # Error Counters
    ###########################################################################

    self.total_errors = 0

    self.analysis_errors = 0
    self.cache_errors = 0

    self.graph_errors = 0

    ###########################################################################
    # Memory Counters
    ###########################################################################

    self.current_memory_mb = 0.0

    self.peak_memory_mb = 0.0

    self.cache_memory_mb = 0.0

    ###########################################################################
    # Health Counters
    ###########################################################################

    self.last_cleanup = 0.0

    self.last_snapshot = 0.0

    self.last_export = 0.0

    self.last_analysis = 0.0

    ###########################################################################
    # Internal Counter Registry
    ###########################################################################

    self._counter_registry = {
        "queries": 0,
        "updates": 0,
        "analyses": 0,
        "traversals": 0,
        "errors": 0,
        "exports": 0,
    }

    self.logger.info(
        "Graph statistics counters initialized successfully."
    )

###############################################################################
# Configuration Initialization
###############################################################################

def _initialize_configuration(self) -> None:
    """
    Initialize Graph Statistics configuration.

    Loads default values, runtime options, analysis settings,
    thresholds, reporting configuration, and feature flags.
    """

    self.logger.debug("Initializing GraphStatistics configuration...")

    ###########################################################################
    # General Configuration
    ###########################################################################

    self.configuration = {

        "version": GRAPH_STATISTICS_VERSION,

        "created_at": self.created_at,

        "lookback_days": DEFAULT_LOOKBACK_DAYS,

        "batch_size": DEFAULT_BATCH_SIZE,

        "timeout": DEFAULT_TIMEOUT,

        "top_n": DEFAULT_TOP_N,

        "cluster_limit": DEFAULT_CLUSTER_LIMIT,
    }

    ###########################################################################
    # Analysis Configuration
    ###########################################################################

    self.analysis_config = {

        "mode": StatisticsMode.STANDARD,

        "compute_degree": True,

        "compute_clusters": True,

        "compute_funding": True,

        "compute_deployer": True,

        "compute_performance": True,

        "compute_cache": True,

        "compute_reports": True,

        "compute_graph_summary": True,
    }

    ###########################################################################
    # Centrality Configuration
    ###########################################################################

    self.centrality_config = {

        "degree": ENABLE_DEGREE_CENTRALITY,

        "betweenness": ENABLE_BETWEENNESS,

        "closeness": ENABLE_CLOSENESS,

        "eigenvector": ENABLE_EIGENVECTOR,

        "pagerank": ENABLE_PAGERANK,

        "iterations": CENTRALITY_MAX_ITERATIONS,

        "tolerance": CENTRALITY_TOLERANCE,
    }

    ###########################################################################
    # Cluster Configuration
    ###########################################################################

    self.cluster_config = {

        "minimum_cluster_size": MIN_CLUSTER_SIZE,

        "large_cluster_threshold": LARGE_CLUSTER_THRESHOLD,

        "mega_cluster_threshold": MEGA_CLUSTER_THRESHOLD,
    }

    ###########################################################################
    # Funding Configuration
    ###########################################################################

    self.funding_config = {

        "minimum_amount": MIN_FUNDING_AMOUNT,

        "maximum_depth": MAX_FUNDING_DEPTH,

        "precision": FUNDING_DECIMAL_PRECISION,

        "high_value_transfer": HIGH_VALUE_TRANSFER,
    }

    ###########################################################################
    # Performance Configuration
    ###########################################################################

    self.performance_config = {

        "memory_warning_mb": MEMORY_WARNING_MB,

        "memory_critical_mb": MEMORY_CRITICAL_MB,

        "sample_size": PERFORMANCE_SAMPLE_SIZE,
    }

    ###########################################################################
    # Export Configuration
    ###########################################################################

    self.export_config = {

        "default_format": ExportFormat.JSON,

        "encoding": EXPORT_ENCODING,

        "indent": EXPORT_JSON_INDENT,

        "include_metadata": True,

        "include_timestamp": True,
    }

    ###########################################################################
    # Runtime Flags
    ###########################################################################

    self.feature_flags = {

        "cache_enabled": True,

        "performance_monitoring": True,

        "snapshot_enabled": True,

        "export_enabled": True,

        "auto_cleanup": True,

        "auto_statistics": True,
    }

    ###########################################################################
    # Internal Runtime State
    ###########################################################################

    self.runtime = {

        "initialized": True,

        "analysis_running": False,

        "building_report": False,

        "snapshotting": False,

        "exporting": False,
    }

    ###########################################################################
    # Database References
    ###########################################################################

    self.database = {

        "graph": self.graph,

        "storage": self.storage,

        "indexes": self.indexes,

        "cache": self.cache,
    }

    ###########################################################################
    # Logger Configuration
    ###########################################################################

    self.logger.info(
        "GraphStatistics configuration initialized successfully."
    )

###############################################################################
# Graph Statistics
###############################################################################

def total_nodes(self) -> int:
    """
    Return total number of nodes currently present in the graph.

    Includes:
        • Wallet nodes
        • Token nodes

    Returns
    -------
    int
        Total node count.
    """

    if self.storage is None:
        return 0

    try:

        total = (
            len(self.storage.wallet_storage)
            + len(self.storage.token_storage)
        )

        self.metrics.total_nodes = total

        self.node_count = total

        self.last_updated = time.time()

        return total

    except Exception as exc:

        self.logger.exception(
            "Failed calculating total nodes: %s",
            exc,
        )

        self.total_errors += 1

        return 0


###############################################################################


def total_edges(self) -> int:
    """
    Return total edge count inside WalletDNA graph.

    Includes:

        • Funding
        • Deployment
        • Transfer
        • Bundle
        • Interaction

    Returns
    -------
    int
        Total edge count.
    """

    if self.indexes is None:
        return 0

    try:

        total = (

            len(self.indexes.funding_index)

            + len(self.indexes.deployment_index)

            + len(self.indexes.transfer_index)

            + len(self.indexes.bundle_index)

            + len(self.indexes.interaction_index)

        )

        self.metrics.total_edges = total

        self.edge_count = total

        self.last_updated = time.time()

        return total

    except Exception as exc:

        self.logger.exception(
            "Failed calculating total edges: %s",
            exc,
        )

        self.total_errors += 1

        return 0

###############################################################################
# Graph Statistics
###############################################################################

def wallet_count(self) -> int:
    """
    Return total wallet nodes stored in the graph.

    Returns
    -------
    int
        Number of wallet nodes.
    """

    if self.storage is None:
        return 0

    try:

        count = len(self.storage.wallet_storage)

        self.metrics.total_wallets = count

        self.wallet_count_counter = count

        self.last_updated = time.time()

        return count

    except Exception as exc:

        self.logger.exception(
            "Failed calculating wallet count: %s",
            exc,
        )

        self.total_errors += 1

        return 0


###############################################################################


def token_count(self) -> int:
    """
    Return total token nodes stored in the graph.

    Returns
    -------
    int
        Number of token nodes.
    """

    if self.storage is None:
        return 0

    try:

        count = len(self.storage.token_storage)

        self.metrics.total_tokens = count

        self.token_count_counter = count

        self.last_updated = time.time()

        return count

    except Exception as exc:

        self.logger.exception(
            "Failed calculating token count: %s",
            exc,
        )

        self.total_errors += 1

        return 0

###############################################################################
# Graph Statistics
###############################################################################

def funding_edge_count(self) -> int:
    """
    Return total funding edges in the graph.

    Returns
    -------
    int
        Number of funding edges.
    """

    if self.indexes is None:
        return 0

    try:

        count = len(self.indexes.funding_index)

        self.metrics.total_funding_edges = count

        self.funding_edge_counter = count

        self.last_updated = time.time()

        return count

    except Exception as exc:

        self.logger.exception(
            "Failed calculating funding edge count: %s",
            exc,
        )

        self.total_errors += 1

        return 0


###############################################################################


def deployment_edge_count(self) -> int:
    """
    Return total deployment edges in the graph.

    Returns
    -------
    int
        Number of deployment edges.
    """

    if self.indexes is None:
        return 0

    try:

        count = len(self.indexes.deployment_index)

        self.metrics.total_deployment_edges = count

        self.deployment_edge_counter = count

        self.last_updated = time.time()

        return count

    except Exception as exc:

        self.logger.exception(
            "Failed calculating deployment edge count: %s",
            exc,
        )

        self.total_errors += 1

        return 0

###############################################################################
# Graph Statistics
###############################################################################

def transfer_edge_count(self) -> int:
    """
    Return total transfer edges in the graph.

    Returns
    -------
    int
        Number of transfer edges.
    """

    if self.indexes is None:
        return 0

    try:

        count = len(self.indexes.transfer_index)

        self.metrics.total_transfer_edges = count

        self.transfer_edge_counter = count

        self.last_updated = time.time()

        return count

    except Exception as exc:

        self.logger.exception(
            "Failed calculating transfer edge count: %s",
            exc,
        )

        self.total_errors += 1

        return 0


###############################################################################


def bundle_edge_count(self) -> int:
 
    Return total bundle edges in the graph.

    Returns
    -------
    int
        Number of bundle edges.
 

    if self.indexes is None:
        return 0

    try:

        count = len(self.indexes.bundle_index)

        self.metrics.total_bundle_edges = count

        self.bundle_edge_counter = count

        self.last_updated = time.time()

        return count

    except Exception as exc:

        self.logger.exception(
            "Failed calculating bundle edge count: %s",
            exc,
        )

        self.total_errors += 1

        return 0


###############################################################################


def interaction_edge_count(self) -> int:
    
    Return total interaction edges in the graph.

    Returns
    -------
    int
        Number of interaction edges.


    if self.indexes is None:
        return 0

    try:

        count = len(self.indexes.interaction_index)

        self.metrics.total_interaction_edges = count

        self.interaction_edge_counter = count

        self.last_updated = time.time()

        return count

    except Exception as exc:

        self.logger.exception(
            "Failed calculating interaction edge count: %s",
            exc,
        )

        self.total_errors += 1

        return 0               

###############################################################################
# Degree Statistics
###############################################################################

def out_degree(self) -> Dict[str, int]:

    Calculate out-degree for every node.

    Returns
    -------
    Dict[str, int]
        Mapping:
            node_id -> out_degree


    if self.graph is None:
        return {}

    try:

        #######################################################################
        # NetworkX Backend
        #######################################################################

        if hasattr(self.graph, "nx_graph"):

            graph = self.graph.nx_graph

            if hasattr(graph, "out_degree"):

                result = {
                    str(node): degree
                    for node, degree in graph.out_degree()
                }

            else:

                result = {
                    str(node): degree
                    for node, degree in graph.degree()
                }

        #######################################################################
        # Rustworkx Backend
        #######################################################################

        elif hasattr(self.graph, "rx_graph"):

            graph = self.graph.rx_graph

            result = {}

            for node in graph.node_indices():

                result[str(node)] = graph.out_degree(node)

        #######################################################################
        # Fallback
        #######################################################################

        else:

            result = {}

        #######################################################################

        self.degree_statistics.out_degree_distribution = result

        self.last_updated = time.time()

        return result

    except Exception as exc:

        self.logger.exception(
            "Failed calculating out-degree: %s",
            exc,
        )

        self.total_errors += 1

        return {}


###############################################################################


def degree_distribution(self) -> Dict[int, int]:
    
    Calculate graph degree distribution.

    Returns
    -------
    Dict[int, int]

        Example

        {
            0: 2,
            1: 15,
            2: 41,
            3: 12,
            4: 5
        }

        degree -> number of nodes
  

    if self.graph is None:
        return {}

    try:

        #######################################################################
        # NetworkX Backend
        #######################################################################

        if hasattr(self.graph, "nx_graph"):

            graph = self.graph.nx_graph

            degrees = [
                degree
                for _, degree in graph.degree()
            ]

        #######################################################################
        # Rustworkx Backend
        #######################################################################

        elif hasattr(self.graph, "rx_graph"):

            graph = self.graph.rx_graph

            degrees = [
                graph.degree(node)
                for node in graph.node_indices()
            ]

        #######################################################################
        # Fallback
        #######################################################################

        else:

            degrees = []

        #######################################################################

        distribution = dict(Counter(degrees))

        self.degree_statistics.degree_distribution = distribution

        self.last_updated = time.time()

        return distribution

    except Exception as exc:

        self.logger.exception(
            "Failed calculating degree distribution: %s",
            exc,
        )

        self.total_errors += 1

        return {}

###############################################################################
# Centrality Statistics
###############################################################################

def degree_centrality(self) -> Dict[str, float]:

    Compute degree centrality for every node.

    Degree Centrality =
        degree(v) / (N - 1)

    Returns
    -------
    Dict[str, float]

        {
            wallet: centrality_score
        }

    if self.graph is None:
        return {}

    try:

        #######################################################################
        # NetworkX Backend
        #######################################################################

        if hasattr(self.graph, "nx_graph"):

            graph = self.graph.nx_graph

            result = nx.degree_centrality(graph)

        #######################################################################
        # Rustworkx Backend
        #######################################################################

        elif hasattr(self.graph, "rx_graph"):

            graph = self.graph.rx_graph

            result = {}

            node_count = len(graph.node_indices())

            if node_count <= 1:

                result = {}

            else:

                denominator = node_count - 1

                for node in graph.node_indices():

                    result[str(node)] = (
                        graph.degree(node)
                        / denominator
                    )

        #######################################################################
        # Fallback
        #######################################################################

        else:

            result = {}

        #######################################################################

        self.centrality_statistics.degree = result

        self.last_updated = time.time()

        return result

    except Exception as exc:

        self.logger.exception(
            "Degree centrality failed: %s",
            exc,
        )

        self.total_errors += 1

        return {}


###############################################################################


def betweenness_centrality(
    self,
    normalized: bool = True,
) -> Dict[str, float]:

    Compute betweenness centrality.

    Measures how


###############################################################################
# Centrality Statistics
###############################################################################

def closeness_centrality(
    self,
    wf_improved: bool = True,
) -> Dict[str, float]:

    Compute closeness centrality.

    Measures how close a node is to every other node.

    Parameters
    ----------
    wf_improved
        Use Wasserman-Faust normalization.

    Returns
    -------
    Dict[str, float]

        {
            wallet: closeness_score
        }

    if self.graph is None:
        return {}

    try:

        #######################################################################
        # NetworkX Backend
        #######################################################################

        if hasattr(self.graph, "nx_graph"):

            graph = self.graph.nx_graph

            result = nx.closeness_centrality(
                graph,
                wf_improved=wf_improved,
            )

        #######################################################################
        # Rustworkx Backend
        #######################################################################

        elif hasattr(self.graph, "rx_graph"):

            graph = self.graph.rx_graph

            result = {}

            for node in graph.node_indices():

                try:

                    lengths = graph.dijkstra_shortest_path_lengths(
                        node,
                        lambda _: 1.0,
                    )

                    if not lengths:

                        result[str(node)] = 0.0
                        continue

                    total_distance = sum(lengths.values())

                    reachable = len(lengths)

                    result[str(node)] = (
                        (reachable - 1) / total_distance
                        if total_distance > 0
                        else 0.0
                    )

                except Exception:

                    result[str(node)] = 0.0

        #######################################################################
        # Fallback
        #######################################################################

        else:

            result = {}

        #######################################################################

        self.centrality_statistics.closeness = result

        self.last_updated = time.time()

        return result

    except Exception as exc:

        self.logger.exception(
            "Closeness centrality failed: %s",
            exc,
        )

        self.total_errors += 1

        return {}


###############################################################################


def eigenvector_centrality(
    self,
    max_iter: int = 100,
    tolerance: float = 1e-6,
) -> Dict[str, float]:

    Compute eigenvector centrality.

    Measures influence by considering the importance
    of neighboring nodes.

    Parameters
    ----------
    max_iter
        Maximum iterations.

    tolerance
        Convergence tolerance.

    Returns
    -------
    Dict[str, float]

        {
            wallet: eigenvector_score
        }

    if self.graph is None:
        return {}

    try:

        #######################################################################
        # NetworkX Backend
        #######################################################################

        if hasattr(self.graph, "nx_graph"):

            graph = self.graph.nx_graph

            result = nx.eigenvector_centrality(
                graph,
                max_iter=max_iter,
                tol=tolerance,
            )

        #######################################################################
        # Rustworkx Backend
        #######################################################################

        elif hasattr(self.graph, "rx_graph"):

            graph = self.graph.rx_graph

            result = {}

            try:

                values = graph.eigenvector_centrality(
                    max_iter=max_iter,
                    tol=tolerance,
                )

                for node, score in zip(
                    graph.node_indices(),
                    values,
                ):

                    result[str(node)] = float(score)

            except Exception:

                result = {}

        #######################################################################
        # Fallback
        #######################################################################

        else:

            result = {}

        #######################################################################

        self.centrality_statistics.eigenvector = result

        self.last_updated = time.time()

        return result

    except Exception as exc:

        self.logger.exception(
            "Eigenvector centrality failed: %s",
            exc,
        )

        self.total_errors += 1

        return {}

###############################################################################
# Centrality Statistics
###############################################################################

def pagerank(
    self,
    alpha: float = 0.85,
    max_iter: int = 100,
    tolerance: float = 1e-6,
) -> Dict[str, float]:
  
    Compute PageRank scores.

    Parameters
    ----------
    alpha
        Damping factor.

    max_iter
        Maximum iterations.

    tolerance
        Convergence tolerance.

    Returns
    -------
    Dict[str, float]

        {
            wallet: pagerank_score
        }

    if self.graph is None:
        return {}

    try:

        #######################################################################
        # NetworkX Backend
        #######################################################################

        if hasattr(self.graph, "nx_graph"):

            graph = self.graph.nx_graph

            result = nx.pagerank(
                graph,
                alpha=alpha,
                max_iter=max_iter,
                tol=tolerance,
            )

        #######################################################################
        # Rustworkx Backend
        #######################################################################

        elif hasattr(self.graph, "rx_graph"):

            graph = self.graph.rx_graph

            result = {}

            try:

                values = graph.pagerank(
                    alpha=alpha,
                    max_iter=max_iter,
                    tol=tolerance,
                )

                for node, score in zip(
                    graph.node_indices(),
                    values,
                ):

                    result[str(node)] = float(score)

            except Exception:

                result = {}

        #######################################################################
        # Fallback
        #######################################################################

        else:

            result = {}

        #######################################################################

        self.centrality_statistics.pagerank = result

        self.last_updated = time.time()

        return result

    except Exception as exc:

        self.logger.exception(
            "PageRank calculation failed: %s",
            exc,
        )

        self.total_errors += 1

        return {}


###############################################################################


def top_central_wallets(
    self,
    metric: str = "pagerank",
    limit: int = 20,
) -> List[Tuple[str, float]]:
   
    Return highest-ranked wallets using selected centrality metric.

    Supported metrics
    -----------------

        degree
        betweenness
        closeness
        eigenvector
        pagerank

    Parameters
    ----------
    metric
        Centrality metric.

    limit
        Number of wallets returned.

    Returns
    -------
    List[Tuple[str, float]]

    try:

        #######################################################################
        # Select Metric
        #######################################################################

        metric_map = {

            "degree":
                self.centrality_statistics.degree,

            "betweenness":
                self.centrality_statistics.betweenness,

            "closeness":
                self.centrality_statistics.closeness,

            "eigenvector":
                self.centrality_statistics.eigenvector,

            "pagerank":
                self.centrality_statistics.pagerank,

        }

        scores = metric_map.get(metric, {})

        if not scores:

            return []

        #######################################################################
        # Sort
        #######################################################################

        ranked = sorted(

            scores.items(),

            key=lambda item: item[1],

            reverse=True,

        )

        top_wallets = ranked[:limit]

        #######################################################################
        # Save Statistics
        #######################################################################

        self.centrality_statistics.top_wallets = top_wallets

        self.last_updated = time.time()

        return top_wallets

    except Exception as exc:

        self.logger.exception(

            "Failed computing top central wallets: %s",

            exc,

        )

        self.total_errors += 1

        return []

###############################################################################
# Cluster Statistics
###############################################################################

def cluster_count(self) -> int:

    Return total number of wallet clusters.

    Uses Cluster Index when available,
    otherwise discovers connected components
    from the graph.

    Returns
    -------
    int
        Total clusters.

    if self.graph is None:
        return 0

    try:

        #######################################################################
        # Cached Cluster Index
        #######################################################################

        if (
            self.indexes is not None
            and self.indexes.cluster_index
        ):

            count = len(self.indexes.cluster_index)

        #######################################################################
        # NetworkX Backend
        #######################################################################

        elif hasattr(self.graph, "nx_graph"):

            graph = self.graph.nx_graph

            if graph.is_directed():

                components = list(
                    nx.weakly_connected_components(
                        graph
                    )
                )

            else:

                components = list(
                    nx.connected_components(
                        graph
                    )
                )

            count = len(components)

        #######################################################################
        # Rustworkx Backend
        #######################################################################

        elif hasattr(self.graph, "rx_graph"):

            graph = self.graph.rx_graph

            components = graph.connected_components()

            count = len(components)

        #######################################################################
        # Fallback
        #######################################################################

        else:

            count = 0

        #######################################################################

        self.cluster_statistics.total_clusters = count

        self.last_updated = time.time()

        return count

    except Exception as exc:

        self.logger.exception(
            "Cluster count failed: %s",
            exc,
        )

        self.total_errors += 1

        return 0


###############################################################################


def largest_cluster(self) -> Tuple[str, int]:

    Return largest wallet cluster.

    Returns
    -------
    Tuple[str, int]

        (
            cluster_id,
            cluster_size
        )
    
    if self.graph is None:
        return ("", 0)

    try:

        #######################################################################
        # Cluster Index
        #######################################################################

        if (
            self.indexes is not None
            and self.indexes.cluster_index
        ):

            cluster_id, wallets = max(

                self.indexes.cluster_index.items(),

                key=lambda item: len(item[1]),

            )

            size = len(wallets)

        #######################################################################
        # NetworkX Backend
        #######################################################################

        elif hasattr(self.graph, "nx_graph"):

            graph = self.graph.nx_graph

            if graph.is_directed():

                components = list(
                    nx.weakly_connected_components(
                        graph
                    )
                )

            else:

                components = list(
                    nx.connected_components(
                        graph
                    )
                )

            if not components:

                return ("", 0)

            largest = max(
                components,
                key=len,
            )

            cluster_id = "cluster_0"

            size = len(largest)

        #######################################################################
        # Rustworkx Backend
        #######################################################################

        elif hasattr(self.graph, "rx_graph"):

            graph = self.graph.rx_graph

            components = graph.connected_components()

            if not components:

                return ("", 0)

            largest = max(
                components,
                key=len,
            )

            cluster_id = "cluster_0"

            size = len(largest)

        #######################################################################
        # Fallback
        #######################################################################

        else:

            return ("", 0)

        #######################################################################

        self.cluster_statistics.largest_cluster_size = size

        self.last_updated = time.time()

        return (cluster_id, size)

    except Exception as exc:

        self.logger.exception(
            "Largest cluster failed: %s",
            exc,
        )

        self.total_errors += 1

        return ("", 0)

###############################################################################
# Funding Statistics
###############################################################################

def average_funding_depth(self) -> float:
   
    Calculate the average funding depth across all wallets.

    Funding depth =
        Number of funding hops from the root funding wallet.

    Returns
    -------
    float
        Average funding depth.

    if self.graph is None:
        return 0.0

    try:

        depths = []

        #######################################################################
        # Cluster Index Traversal
        #######################################################################

        if self.indexes is not None:

            for wallet in self.indexes.wallet_index.keys():

                try:

                    depth = self.graph.funding_depth(wallet)

                    depths.append(depth)

                except Exception:

                    continue

        #######################################################################

        if not depths:

            average = 0.0

        else:

            average = sum(depths) / len(depths)

        #######################################################################

        self.funding_statistics.average_depth = average

        self.last_updated = time.time()

        return round(average, 4)

    except Exception as exc:

        self.logger.exception(
            "Average funding depth failed: %s",
            exc,
        )

        self.total_errors += 1

        return 0.0


###############################################################################


def maximum_funding_depth(self) -> int:

    Return deepest funding chain discovered.

    Returns
    -------
    int
        Maximum funding depth.

    if self.graph is None:
        return 0

    try:

        maximum = 0

        #######################################################################
        # Wallet Traversal
        #######################################################################

        if self.indexes is not None:

            for wallet in self.indexes.wallet_index.keys():

                try:

                    depth = self.graph.funding_depth(wallet)

                    if depth > maximum:

                        maximum = depth

                except Exception:

                    continue

        #######################################################################

        self.funding_statistics.maximum_depth = maximum

        self.last_updated = time.time()

        return maximum

    except Exception as exc:

        self.logger.exception(
            "Maximum funding depth failed: %s",
            exc,
        )

        self.total_errors += 1

        return 0                        

###############################################################################
# Funding Statistics
###############################################################################

def funding_sources(self) -> Dict[str, int]:

    Calculate funding source frequency.

    Returns
    -------
    Dict[str, int]

        {
            funding_wallet: number_of_wallets_funded
        }


    if self.indexes is None:
        return {}

    try:

        sources: Dict[str, int] = {}

        #######################################################################
        # Funding Index
        #######################################################################

        for source, edges in self.indexes.funding_index.items():

            if isinstance(edges, (list, set, tuple)):

                sources[str(source)] = len(edges)

            else:

                sources[str(source)] = 1

        #######################################################################

        self.funding_statistics.sources = sources

        self.last_updated = time.time()

        return sources

    except Exception as exc:

        self.logger.exception(
            "Funding source statistics failed: %s",
            exc,
        )

        self.total_errors += 1

        return {}


###############################################################################


def funding_destinations(self) -> Dict[str, int]:

    Calculate funding destination frequency.

    Returns
    -------
    Dict[str, int]

        {
            wallet: number_of_funding_sources
        }

    if self.indexes is None:
        return {}

    try:

        destinations: Dict[str, int] = {}

        #######################################################################
        # Funding Index Traversal
        #######################################################################

        for _, edges in self.indexes.funding_index.items():

            if not isinstance(edges, (list, tuple, set)):

                edges = [edges]

            for edge in edges:

                ################################################################
                # FundingEdge object
                ################################################################

                if hasattr(edge, "destination"):

                    wallet = str(edge.destination)

                elif hasattr(edge, "to_wallet"):

                    wallet = str(edge.to_wallet)

                elif hasattr(edge, "target"):

                    wallet = str(edge.target)

                else:

                    continue

                destinations[wallet] = (
                    destinations.get(wallet, 0) + 1
                )

        #######################################################################

        self.funding_statistics.destinations = destinations

        self.last_updated = time.time()

        return destinations

    except Exception as exc:

        self.logger.exception(
            "Funding destination statistics failed: %s",
            exc,
        )

        self.total_errors += 1

        return {}

###############################################################################
# Deployer Statistics
###############################################################################

def deployer_count(self) -> int:
  
    Return total number of deployer wallets.

    A deployer wallet is defined as a wallet that has
    deployed at least one token.

    Returns
    -------
    int
        Total deployers.

    if self.storage is None:
        return 0

    try:

        deployers = 0

        #######################################################################
        # Wallet Storage
        #######################################################################

        for wallet in self.storage.wallet_storage.values():

            if getattr(wallet, "tokens_deployed", 0) > 0:

                deployers += 1

        #######################################################################

        self.deployer_statistics.total_deployers = deployers

        self.last_updated = time.time()

        return deployers

    except Exception as exc:

        self.logger.exception(
            "Failed calculating deployer count: %s",
            exc,
        )

        self.total_errors += 1

        return 0


###############################################################################


def average_launches(self) -> float:
    
    Calculate average number of launches per deployer.

    Returns
    -------
    float
        Average launches.


    if self.storage is None:
        return 0.0

    try:

        launches = []

        #######################################################################
        # Wallet Storage
        #######################################################################

        for wallet in self.storage.wallet_storage.values():

            deployed = getattr(
                wallet,
                "tokens_deployed",
                0,
            )

            if deployed > 0:

                launches.append(deployed)

        #######################################################################

        if not launches:

            average = 0.0

        else:

            average = sum(launches) / len(launches)

        #######################################################################

        self.deployer_statistics.average_launches = average

        self.last_updated = time.time()

        return round(average, 4)

    except Exception as exc:

        self.logger.exception(
            "Failed calculating average launches: %s",
            exc,
        )

        self.total_errors += 1

        return 0.0

###############################################################################
# Deployer Statistics
###############################################################################

def successful_launches(
    self,
    minimum_marketcap: float = 100_000.0,
) -> Dict[str, int]:
    """
    Calculate successful launches for every deployer.

    A launch is considered successful when its
    market cap reaches at least `minimum_marketcap`.

    Parameters
    ----------
    minimum_marketcap : float
        Success threshold.

    Returns
    -------
    Dict[str, int]

        {
            deployer_wallet: successful_launches
        }
    """

    if self.storage is None:
        return {}

    try:

        successful: Dict[str, int] = {}

        #######################################################################
        # Token Storage
        #######################################################################

        for token in self.storage.token_storage.values():

            deployer = getattr(
                token,
                "deployer",
                None,
            )

            if deployer is None:
                continue

            marketcap = float(
                getattr(
                    token,
                    "market_cap",
                    0.0,
                )
            )

            if marketcap >= minimum_marketcap:

                successful[deployer] = (
                    successful.get(deployer, 0) + 1
                )

        #######################################################################

        self.deployer_statistics.successful_launches = successful

        self.last_updated = time.time()

        return successful

    except Exception as exc:

        self.logger.exception(
            "Failed calculating successful launches: %s",
            exc,
        )

        self.total_errors += 1

        return {}


###############################################################################


def rug_rate(self) -> Dict[str, float]:
    """
    Calculate rug rate for every deployer.

    Rug Rate

        rugs / total launches

    Returns
    -------
    Dict[str, float]

        {
            deployer_wallet: rug_rate
        }
    """

    if self.storage is None:
        return {}

    try:

        rugs: Dict[str, int] = {}

        launches: Dict[str, int] = {}

        #######################################################################
        # Token Storage
        #######################################################################

        for token in self.storage.token_storage.values():

            deployer = getattr(
                token,
                "deployer",
                None,
            )

            if deployer is None:
                continue

            launches[deployer] = (
                launches.get(deployer, 0) + 1
            )

            ###############################################################
            # Rug Detection
            ###############################################################

            is_rug = bool(

                getattr(token, "is_rug", False)

                or getattr(token, "rugged", False)

                or getattr(token, "rug_detected", False)

            )

            if is_rug:

                rugs[deployer] = (
                    rugs.get(deployer, 0) + 1
                )

        #######################################################################
        # Compute Rug Rate
        #######################################################################

        rug_rates: Dict[str, float] = {}

        for deployer, total in launches.items():

            rug_count = rugs.get(deployer, 0)

            rug_rates[deployer] = (
                rug_count / total
                if total > 0
                else 0.0
            )

        #######################################################################

        self.deployer_statistics.rug_rates = rug_rates

        self.last_updated = time.time()

        return rug_rates

    except Exception as exc:

        self.logger.exception(
            "Failed calculating rug rates: %s",
            exc,
        )

        self.total_errors += 1

        return {}        

###############################################################################
# Deployer Statistics
###############################################################################

def reputation_distribution(self) -> Dict[str, List[str]]:
    """
    Categorize deployers into reputation tiers.

    Reputation Score

        score =
            (successful_launches / total_launches)
            * (1 - rug_rate)

    Reputation Tiers

        Elite      >= 0.90
        Excellent  >= 0.75
        Good       >= 0.60
        Average    >= 0.40
        Risky      >= 0.20
        Malicious  < 0.20

    Returns
    -------
    Dict[str, List[str]]

        {
            "elite": [...],
            "excellent": [...],
            "good": [...],
            "average": [...],
            "risky": [...],
            "malicious": [...]
        }
    """

    if self.storage is None:
        return {}

    try:

        #######################################################################
        # Statistics
        #######################################################################

        successful = self.successful_launches()

        rug_rates = self.rug_rate()

        distribution = {

            "elite": [],
            "excellent": [],
            "good": [],
            "average": [],
            "risky": [],
            "malicious": [],

        }

        #######################################################################
        # Calculate Reputation
        #######################################################################

        for wallet in self.storage.wallet_storage.values():

            deployer = getattr(
                wallet,
                "address",
                None,
            )

            if deployer is None:
                continue

            launches = getattr(
                wallet,
                "tokens_deployed",
                0,
            )

            if launches == 0:
                continue

            success = successful.get(
                deployer,
                0,
            )

            rug_rate = rug_rates.get(
                deployer,
                0.0,
            )

            success_rate = success / launches

            reputation = success_rate * (1.0 - rug_rate)

            ###############################################################
            # Reputation Tier
            ###############################################################

            if reputation >= 0.90:

                distribution["elite"].append(deployer)

            elif reputation >= 0.75:

                distribution["excellent"].append(deployer)

            elif reputation >= 0.60:

                distribution["good"].append(deployer)

            elif reputation >= 0.40:

                distribution["average"].append(deployer)

            elif reputation >= 0.20:

                distribution["risky"].append(deployer)

            else:

                distribution["malicious"].append(deployer)

        #######################################################################
        # Store Statistics
        #######################################################################

        self.deployer_statistics.reputation_distribution = distribution

        self.deployer_statistics.reputation_counts = {

            tier: len(wallets)
            for tier, wallets in distribution.items()

        }

        self.last_updated = time.time()

        return distribution

    except Exception as exc:

        self.logger.exception(
            "Failed calculating reputation distribution: %s",
            exc,
        )

        self.total_errors += 1

        return {}        

###############################################################################
# Performance Statistics
###############################################################################

import sys
from collections import deque
from typing import Any


def graph_memory(self) -> int:
    """
    Calculate approximate graph memory usage.

    Includes
    --------
    • Wallet storage
    • Token storage
    • Node registry
    • Graph backend

    Returns
    -------
    int
        Memory usage in bytes.
    """

    try:

        visited = set()

        #######################################################################
        # Recursive sizeof
        #######################################################################

        def sizeof(obj: Any) -> int:

            obj_id = id(obj)

            if obj_id in visited:
                return 0

            visited.add(obj_id)

            size = sys.getsizeof(obj)

            ###############################################################
            # Dictionaries
            ###############################################################

            if isinstance(obj, dict):

                size += sum(
                    sizeof(k) + sizeof(v)
                    for k, v in obj.items()
                )

            ###############################################################
            # Iterable containers
            ###############################################################

            elif isinstance(
                obj,
                (
                    list,
                    tuple,
                    set,
                    frozenset,
                    deque,
                ),
            ):

                size += sum(
                    sizeof(item)
                    for item in obj
                )

            ###############################################################
            # Objects
            ###############################################################

            elif hasattr(obj, "__dict__"):

                size += sizeof(vars(obj))

            return size

        #######################################################################
        # Graph Components
        #######################################################################

        total = 0

        if getattr(self, "storage", None):

            total += sizeof(self.storage)

        if getattr(self, "graph", None):

            total += sizeof(self.graph)

        if getattr(self, "indexes", None):

            total += sizeof(self.indexes)

        #######################################################################

        self.performance_statistics.graph_memory = total

        self.last_updated = time.time()

        return total

    except Exception as exc:

        self.logger.exception(
            "Graph memory calculation failed: %s",
            exc,
        )

        self.total_errors += 1

        return 0


###############################################################################


def cache_memory(self) -> int:
    """
    Calculate total cache memory usage.

    Includes
    --------
    • DFS cache
    • BFS cache
    • Shortest-path cache
    • Funding cache
    • Centrality cache
    • Cluster cache

    Returns
    -------
    int
        Memory usage in bytes.
    """

    try:

        if getattr(self, "cache", None) is None:
            return 0

        visited = set()

        #######################################################################
        # Recursive sizeof
        #######################################################################

        def sizeof(obj: Any) -> int:

            obj_id = id(obj)

            if obj_id in visited:
                return 0

            visited.add(obj_id)

            size = sys.getsizeof(obj)

            if isinstance(obj, dict):

                size += sum(
                    sizeof(k) + sizeof(v)
                    for k, v in obj.items()
                )

            elif isinstance(
                obj,
                (
                    list,
                    tuple,
                    set,
                    frozenset,
                    deque,
                ),
            ):

                size += sum(
                    sizeof(item)
                    for item in obj
                )

            elif hasattr(obj, "__dict__"):

                size += sizeof(vars(obj))

            return size

        #######################################################################

        total = sizeof(self.cache)

        self.performance_statistics.cache_memory = total

        self.last_updated = time.time()

        return total

    except Exception as exc:

        self.logger.exception(
            "Cache memory calculation failed: %s",
            exc,
        )

        self.total_errors += 1

        return 0

###############################################################################
# Performance Statistics
###############################################################################

def build_time(self) -> float:
    """
    Return graph build time.

    Returns
    -------
    float
        Graph build time in seconds.
    """

    try:

        #######################################################################
        # Cached Value
        #######################################################################

        build_time = getattr(
            self.performance_statistics,
            "graph_build_time",
            None,
        )

        if build_time is None:

            build_time = getattr(
                self,
                "_graph_build_time",
                0.0,
            )

        #######################################################################

        build_time = float(build_time)

        self.performance_statistics.graph_build_time = build_time

        self.last_updated = time.time()

        return round(build_time, 6)

    except Exception as exc:

        self.logger.exception(
            "Build time calculation failed: %s",
            exc,
        )

        self.total_errors += 1

        return 0.0


###############################################################################


def traversal_time(self) -> Dict[str, float]:
    """
    Return traversal performance statistics.

    Includes

        DFS
        BFS
        Shortest Path
        Funding Traversal

    Returns
    -------
    Dict[str, float]
    """

    try:

        traversal = {

            "dfs": getattr(
                self,
                "_dfs_time",
                0.0,
            ),

            "bfs": getattr(
                self,
                "_bfs_time",
                0.0,
            ),

            "shortest_path": getattr(
                self,
                "_shortest_path_time",
                0.0,
            ),

            "funding": getattr(
                self,
                "_funding_time",
                0.0,
            ),

        }

        #######################################################################
        # Average Traversal
        #######################################################################

        values = list(traversal.values())

        traversal["average"] = (

            sum(values) / len(values)

            if values

            else 0.0

        )

        #######################################################################

        self.performance_statistics.traversal_times = traversal

        self.last_updated = time.time()

        return traversal

    except Exception as exc:

        self.logger.exception(
            "Traversal statistics failed: %s",
            exc,
        )

        self.total_errors += 1

        return {
            "dfs": 0.0,
            "bfs": 0.0,
            "shortest_path": 0.0,
            "funding": 0.0,
            "average": 0.0,
        }

###############################################################################
# Performance Statistics
###############################################################################

def cache_hit_rate(self) -> float:
    """
    Calculate cache hit rate.

    Formula
    -------
        hit_rate = cache_hits / (cache_hits + cache_misses)

    Returns
    -------
    float
        Cache hit rate between 0.0 and 1.0
    """

    try:

        #######################################################################
        # Read Statistics
        #######################################################################

        if getattr(self, "cache", None) is not None:

            stats = self.cache.statistics()

            hits = int(stats.get("hits", 0))

            misses = int(stats.get("misses", 0))

        else:

            hits = getattr(self, "cache_hits", 0)

            misses = getattr(self, "cache_misses", 0)

        #######################################################################

        total = hits + misses

        if total == 0:

            rate = 0.0

        else:

            rate = hits / total

        #######################################################################

        self.performance_statistics.cache_hit_rate = rate

        self.last_updated = time.time()

        return round(rate, 4)

    except Exception as exc:

        self.logger.exception(
            "Cache hit rate calculation failed: %s",
            exc,
        )

        self.total_errors += 1

        return 0.0


###############################################################################


def throughput(self) -> Dict[str, float]:
      Calculate Wallet DNA processing throughput.

    Metrics
    -------
    nodes_per_second
    edges_per_second
    wallets_per_second
    tokens_per_second

    Returns
    -------
    Dict[str, float]


    try:

        #######################################################################
        # Build Time
        #######################################################################

        build_seconds = self.build_time()

        if build_seconds <= 0:

            build_seconds = 1e-9

        #######################################################################
        # Counts
        #######################################################################

        nodes = self.total_nodes()

        edges = self.total_edges()

        wallets = self.wallet_count()

        tokens = self.token_count()

        #######################################################################
        # Throughput
        #######################################################################

        metrics = {

            "nodes_per_second":
                nodes / build_seconds,

            "edges_per_second":
                edges / build_seconds,

            "wallets_per_second":
                wallets / build_seconds,

            "tokens_per_second":
                tokens / build_seconds,

        }

        #######################################################################

        self.performance_statistics.throughput = metrics

        self.last_updated = time.time()

        return metrics

    except Exception as exc:

        self.logger.exception(
            "Throughput calculation failed: %s",
            exc,
        )

        self.total_errors += 1

        return {

            "nodes_per_second": 0.0,

            "edges_per_second": 0.0,

            "wallets_per_second": 0.0,

            "tokens_per_second": 0.0,

        }

###############################################################################
# Reports
###############################################################################

def summary(self) -> GraphSummary:
    
    Generate a high-level summary of the Wallet DNA graph.

    Returns
    -------
    GraphSummary
        Consolidated graph statistics.
    

    try:

        summary = GraphSummary(

            ###################################################################
            # Graph
            ###################################################################

            total_nodes=self.total_nodes(),

            total_edges=self.total_edges(),

            wallet_count=self.wallet_count(),

            token_count=self.token_count(),

            ###################################################################
            # Degree
            ###################################################################

            average_degree=self.average_degree(),

            maximum_degree=self.max_degree(),

            minimum_degree=self.min_degree(),

            ###################################################################
            # Clusters
            ###################################################################

            total_clusters=self.cluster_count(),

            largest_cluster=self.largest_cluster(),

            ###################################################################
            # Funding
            ###################################################################

            average_funding_depth=self.average_funding_depth(),

            maximum_funding_depth=self.maximum_funding_depth(),

            ###################################################################
            # Deployers
            ###################################################################

            deployer_count=self.deployer_count(),

            average_launches=self.average_launches(),

            ###################################################################
            # Performance
            ###################################################################

            graph_memory=self.graph_memory(),

            cache_memory=self.cache_memory(),

            build_time=self.build_time(),

            cache_hit_rate=self.cache_hit_rate(),

        )

        #######################################################################

        self.last_updated = time.time()

        return summary

    except Exception as exc:

        self.logger.exception(
            "Failed generating graph summary: %s",
            exc,
        )

        self.total_errors += 1

        return GraphSummary()

###############################################################################
# Reports
###############################################################################

def graph_report(self) -> GraphReport:
    """
    Generate a complete Wallet DNA graph report.

    This is the master report containing every major
    statistics model produced by the graph engine.

    Returns
    -------
    GraphReport
        Complete graph report.
    """

    try:

        #######################################################################
        # Basic Summary
        #######################################################################

        summary = self.summary()

        #######################################################################
        # Degree Statistics
        #######################################################################

        degree_statistics = DegreeStatistics(

            average_degree=self.average_degree(),

            maximum_degree=self.max_degree(),

            minimum_degree=self.min_degree(),

            degree_distribution=self.degree_distribution(),

        )

        #######################################################################
        # Centrality Statistics
        #######################################################################

        centrality_statistics = CentralityStatistics(

            degree=self.degree_centrality(),

            betweenness=self.betweenness_centrality(),

            closeness=self.closeness_centrality(),

            eigenvector=self.eigenvector_centrality(),

            pagerank=self.pagerank(),

            top_wallets=self.top_central_wallets(),

        )

        #######################################################################
        # Cluster Statistics
        #######################################################################

        cluster_statistics = ClusterStatistics(

            total_clusters=self.cluster_count(),

            largest_cluster=self.largest_cluster(),

            average_cluster_size=self.average_cluster_size(),

            isolated_wallets=self.isolated_wallets(),

            distribution=self.cluster_distribution(),

        )

        #######################################################################
        # Funding Statistics
        #######################################################################

        funding_statistics = FundingStatistics(

            average_depth=self.average_funding_depth(),

            maximum_depth=self.maximum_funding_depth(),

            funding_sources=self.funding_sources(),

            funding_destinations=self.funding_destinations(),

            tree_sizes=self.funding_tree_size(),

        )

        #######################################################################
        # Deployer Statistics
        #######################################################################

        deployer_statistics = DeployerStatistics(

            total_deployers=self.deployer_count(),

            average_launches=self.average_launches(),

            successful_launches=self.successful_launches(),

            rug_rates=self.rug_rate(),

            reputation_distribution=self.reputation_distribution(),

        )

        #######################################################################
        # Performance Statistics
        #######################################################################

        performance_statistics = PerformanceStatistics(

            graph_memory=self.graph_memory(),

            cache_memory=self.cache_memory(),

            graph_build_time=self.build_time(),

            traversal_times=self.traversal_time(),

            cache_hit_rate=self.cache_hit_rate(),

            throughput=self.throughput(),

        )

        #######################################################################
        # Cache Statistics
        #######################################################################

        cache_statistics = CacheStatistics()

        if getattr(self, "cache", None):

            cache_info = self.cache.statistics()

            cache_statistics.hits = cache_info.get("hits", 0)

            cache_statistics.misses = cache_info.get("misses", 0)

            cache_statistics.hit_rate = cache_info.get(
                "hit_rate",
                self.cache_hit_rate(),
            )

        #######################################################################
        # Build Report
        #######################################################################

        report = GraphReport(

            generated_at=time.time(),

            summary=summary,

            degree_statistics=degree_statistics,

            centrality_statistics=centrality_statistics,

            cluster_statistics=cluster_statistics,

            funding_statistics=funding_statistics,

            deployer_statistics=deployer_statistics,

            performance_statistics=performance_statistics,

            cache_statistics=cache_statistics,

        )

        #######################################################################

        self.last_updated = time.time()

        return report

    except Exception as exc:

        self.logger.exception(
            "Failed generating graph report: %s",
            exc,
        )

        self.total_errors += 1

        return GraphReport()

###############################################################################
# Reports
###############################################################################

def funding_report(self) -> Dict[str, Any]:
    """
    Generate a comprehensive funding report.

    Returns
    -------
    Dict[str, Any]
        Funding analytics report.
    """

    try:

        average_depth = self.average_funding_depth()
        maximum_depth = self.maximum_funding_depth()

        funding_sources = self.funding_sources()
        funding_destinations = self.funding_destinations()
        funding_tree_sizes = self.funding_tree_size()

        top_sources = sorted(
            funding_sources.items(),
            key=lambda item: item[1],
            reverse=True
        )[:20]

        top_destinations = sorted(
            funding_destinations.items(),
            key=lambda item: item[1],
            reverse=True
        )[:20]

        largest_trees = sorted(
            funding_tree_sizes.items(),
            key=lambda item: item[1],
            reverse=True
        )[:20]

        report = {
            "generated_at": time.time(),

            "summary": {
                "average_funding_depth": average_depth,
                "maximum_funding_depth": maximum_depth,
                "unique_funding_sources": len(funding_sources),
                "unique_funding_destinations": len(funding_destinations),
                "funding_tree_count": len(funding_tree_sizes),
            },

            "statistics": {
                "funding_sources": funding_sources,
                "funding_destinations": funding_destinations,
                "funding_tree_sizes": funding_tree_sizes,
            },

            "rankings": {
                "top_sources": top_sources,
                "top_destinations": top_destinations,
                "largest_funding_trees": largest_trees,
            },
        }

        self.last_updated = time.time()

        return report

    except Exception as exc:

        self.logger.exception(
            "Funding report generation failed: %s",
            exc,
        )

        self.total_errors += 1

        return {
            "generated_at": time.time(),
            "summary": {},
            "statistics": {},
            "rankings": {},
        }

###############################################################################
# Reports
###############################################################################

def deployer_report(self) -> Dict[str, Any]:
    """
    Generate a comprehensive deployer report.

    Includes launch performance, rug statistics,
    reputation analysis, and top deployers.

    Returns
    -------
    Dict[str, Any]
        Deployer analytics report.
    """

    try:

        #######################################################################
        # Core Statistics
        #######################################################################

        deployer_count = self.deployer_count()

        average_launches = self.average_launches()

        successful_launches = self.successful_launches()

        rug_rates = self.rug_rate()

        reputation = self.reputation_distribution()

        #######################################################################
        # Launch Count
        #######################################################################

        total_launches = {}

        for wallet in self.storage.wallet_storage.values():

            address = getattr(wallet, "address", None)

            launches = getattr(wallet, "tokens_deployed", 0)

            if address is None or launches == 0:

                continue

            total_launches[address] = launches

        #######################################################################
        # Top Deployers
        #######################################################################

        top_deployers = sorted(

            total_launches.items(),

            key=lambda item: item[1],

            reverse=True,

        )[:20]

        #######################################################################
        # Most Successful Deployers
        #######################################################################

        top_successful = sorted(

            successful_launches.items(),

            key=lambda item: item[1],

            reverse=True,

        )[:20]

        #######################################################################
        # Lowest Rug Rate
        #######################################################################

        safest_deployers = sorted(

            rug_rates.items(),

            key=lambda item: item[1],

        )[:20]

        #######################################################################
        # Highest Rug Rate
        #######################################################################

        riskiest_deployers = sorted(

            rug_rates.items(),

            key=lambda item: item[1],

            reverse=True,

        )[:20]

        #######################################################################
        # Report
        #######################################################################

        report = {

            "generated_at": time.time(),

            "summary": {

                "total_deployers": deployer_count,

                "average_launches": average_launches,

                "successful_deployers": len(successful_launches),

            },

            "statistics": {

                "launches": total_launches,

                "successful_launches": successful_launches,

                "rug_rates": rug_rates,

                "reputation_distribution": reputation,

            },

            "rankings": {

                "top_deployers": top_deployers,

                "top_successful": top_successful,

                "safest_deployers": safest_deployers,

                "riskiest_deployers": riskiest_deployers,

            },

        }

        #######################################################################

        self.last_updated = time.time()

        return report

    except Exception as exc:

        self.logger.exception(

            "Deployer report generation failed: %s",

            exc,

        )

        self.total_errors += 1

        return {

            "generated_at": time.time(),

            "summary": {},

            "statistics": {},

            "rankings": {},

        }

###############################################################################
# Reports
###############################################################################

def export_statistics(
    self,
    file_path: Optional[str] = None,
    format: str = "json",
) -> Union[Dict[str, Any], str]:
    """
    Export all Wallet DNA statistics.

    Supported Formats
    -----------------
        json
        yaml
        csv

    Parameters
    ----------
    file_path : Optional[str]
        Output file path.

    format : str
        Export format.

    Returns
    -------
    Dict[str, Any] | str
    """

    try:

        #######################################################################
        # Collect Everything
        #######################################################################

        export_data = {

            "generated_at": time.time(),

            "summary":
                asdict(self.summary()),

            "graph_report":
                asdict(self.graph_report()),

            "funding_report":
                self.funding_report(),

            "deployer_report":
                self.deployer_report(),

            "performance": {

                "graph_memory":
                    self.graph_memory(),

                "cache_memory":
                    self.cache_memory(),

                "build_time":
                    self.build_time(),

                "traversal_time":
                    self.traversal_time(),

                "cache_hit_rate":
                    self.cache_hit_rate(),

                "throughput":
                    self.throughput(),

            },

        }

        #######################################################################
        # No File → Return Dictionary
        #######################################################################

        if file_path is None:

            return export_data

        #######################################################################
        # JSON
        #######################################################################

        if format.lower() == "json":

            with open(
                file_path,
                "w",
                encoding="utf-8",
            ) as fp:

                json.dump(

                    export_data,

                    fp,

                    indent=4,

                    default=str,

                )

        #######################################################################
        # YAML
        #######################################################################

        elif format.lower() == "yaml":

            try:

                import yaml

            except ImportError:

                raise ImportError(
                    "PyYAML is required for YAML export."
                )

            with open(
                file_path,
                "w",
                encoding="utf-8",
            ) as fp:

                yaml.safe_dump(

                    export_data,

                    fp,

                    sort_keys=False,

                    default_flow_style=False,

                )

        #######################################################################
        # CSV
        #######################################################################

        elif format.lower() == "csv":

            with open(

                file_path,

                "w",

                newline="",

                encoding="utf-8",

            ) as fp:

                writer = csv.writer(fp)

                writer.writerow(
                    ["Metric", "Value"]
                )

                for key, value in export_data["summary"].items():

                    writer.writerow(
                        [key, value]
                    )

        #######################################################################
        # Invalid
        #######################################################################

        else:

            raise ValueError(
                f"Unsupported export format: {format}"
            )

        #######################################################################

        self.last_updated = time.time()

        self.logger.info(

            "Statistics exported to %s",

            file_path,

        )

        return file_path

    except Exception as exc:

        self.logger.exception(

            "Statistics export failed: %s",

            exc,

        )

        self.total_errors += 1

        raise

###############################################################################
# Utilities
###############################################################################

def reset(self) -> None:
    """
    Reset all runtime statistics.

    This does NOT modify the Wallet DNA graph.

    It only clears computed statistics,
    counters, timing information and caches.

    Returns
    -------
    None
    """

    try:

        #######################################################################
        # Statistics Models
        #######################################################################

        self.graph_metrics = GraphMetrics()

        self.degree_statistics = DegreeStatistics()

        self.centrality_statistics = CentralityStatistics()

        self.cluster_statistics = ClusterStatistics()

        self.funding_statistics = FundingStatistics()

        self.deployer_statistics = DeployerStatistics()

        self.performance_statistics = PerformanceStatistics()

        self.cache_statistics = CacheStatistics()

        #######################################################################
        # Runtime Metrics
        #######################################################################

        self._initialize_metrics()

        #######################################################################
        # Runtime Counters
        #######################################################################

        self._initialize_counters()

        #######################################################################
        # Cache Reset
        #######################################################################

        if getattr(self, "cache", None):

            self.cache.clear_all()

        #######################################################################
        # Timestamp
        #######################################################################

        self.last_updated = time.time()

        #######################################################################
        # Logger
        #######################################################################

        self.logger.info(
            "Graph statistics successfully reset."
        )

    except Exception as exc:

        self.logger.exception(
            "Failed to reset graph statistics: %s",
            exc,
        )

        self.total_errors += 1

        raise


###############################################################################
# Utilities
###############################################################################

def snapshot(self) -> StatisticsSnapshot:
    """
    Create a complete snapshot of the current graph statistics.

    This snapshot can later be restored using
    restore().

    Returns
    -------
    StatisticsSnapshot
        Immutable snapshot of all statistics.
    """

    try:

        #######################################################################
        # Build Snapshot
        #######################################################################

        snapshot = StatisticsSnapshot(

            timestamp=time.time(),

            graph_metrics=copy.deepcopy(
                self.graph_metrics
            ),

            degree_statistics=copy.deepcopy(
                self.degree_statistics
            ),

            centrality_statistics=copy.deepcopy(
                self.centrality_statistics
            ),

            cluster_statistics=copy.deepcopy(
                self.cluster_statistics
            ),

            funding_statistics=copy.deepcopy(
                self.funding_statistics
            ),

            deployer_statistics=copy.deepcopy(
                self.deployer_statistics
            ),

            performance_statistics=copy.deepcopy(
                self.performance_statistics
            ),

            cache_statistics=copy.deepcopy(
                self.cache_statistics
            ),

            runtime_metrics={

                "last_updated":
                    self.last_updated,

                "total_errors":
                    self.total_errors,

                "cache_hits":
                    getattr(
                        self,
                        "cache_hits",
                        0,
                    ),

                "cache_misses":
                    getattr(
                        self,
                        "cache_misses",
                        0,
                    ),

            },

        )

        #######################################################################
        # Store Latest Snapshot
        #######################################################################

        self.latest_snapshot = snapshot

        self.last_updated = time.time()

        self.logger.info(
            "Statistics snapshot created successfully."
        )

        return snapshot

    except Exception as exc:

        self.logger.exception(
            "Failed to create statistics snapshot: %s",
            exc,
        )

        self.total_errors += 1

        raise


###############################################################################
# Utilities
###############################################################################

def restore(
    self,
    snapshot: Optional[StatisticsSnapshot] = None,
) -> bool:
    """
    Restore graph statistics from a previously created snapshot.

    Parameters
    ----------
    snapshot : StatisticsSnapshot, optional
        Snapshot to restore.
        If None, restores the latest snapshot.

    Returns
    -------
    bool
        True if restoration succeeds.
    """

    try:

        #######################################################################
        # Select Snapshot
        #######################################################################

        if snapshot is None:

            snapshot = getattr(
                self,
                "latest_snapshot",
                None,
            )

        if snapshot is None:

            self.logger.warning(
                "No statistics snapshot available."
            )

            return False

        #######################################################################
        # Restore Statistics Models
        #######################################################################

        self.graph_metrics = copy.deepcopy(
            snapshot.graph_metrics
        )

        self.degree_statistics = copy.deepcopy(
            snapshot.degree_statistics
        )

        self.centrality_statistics = copy.deepcopy(
            snapshot.centrality_statistics
        )

        self.cluster_statistics = copy.deepcopy(
            snapshot.cluster_statistics
        )

        self.funding_statistics = copy.deepcopy(
            snapshot.funding_statistics
        )

        self.deployer_statistics = copy.deepcopy(
            snapshot.deployer_statistics
        )

        self.performance_statistics = copy.deepcopy(
            snapshot.performance_statistics
        )

        self.cache_statistics = copy.deepcopy(
            snapshot.cache_statistics
        )

        #######################################################################
        # Restore Runtime Metrics
        #######################################################################

        runtime = snapshot.runtime_metrics

        self.last_updated = runtime.get(
            "last_updated",
            time.time(),
        )

        self.total_errors = runtime.get(
            "total_errors",
            0,
        )

        self.cache_hits = runtime.get(
            "cache_hits",
            0,
        )

        self.cache_misses = runtime.get(
            "cache_misses",
            0,
        )

        #######################################################################
        # Logging
        #######################################################################

        self.logger.info(
            "Statistics restored successfully."
        )

        return True

    except Exception as exc:

        self.logger.exception(
            "Failed restoring statistics: %s",
            exc,
        )

        self.total_errors += 1

        return False

###############################################################################
# Utilities
###############################################################################

def pretty_print(self) -> str:
    """
    Generate a human-readable statistics report.

    Returns
    -------
    str
        Formatted statistics report.
    """

    try:

        separator = "=" * 80

        report = []

        #######################################################################
        # Header
        #######################################################################

        report.append(separator)
        report.append("                 SENTINEL AI — WALLET DNA GRAPH REPORT")
        report.append(separator)

        report.append(
            f"Generated : {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}"
        )

        report.append("")

        #######################################################################
        # Graph Statistics
        #######################################################################

        report.append("[GRAPH]")

        report.append(
            f"Total Nodes              : {self.total_nodes()}"
        )

        report.append(
            f"Total Edges              : {self.total_edges()}"
        )

        report.append(
            f"Wallets                  : {self.wallet_count()}"
        )

        report.append(
            f"Tokens                   : {self.token_count()}"
        )

        report.append("")

        #######################################################################
        # Degree Statistics
        #######################################################################

        report.append("[DEGREE]")

        report.append(
            f"Average Degree           : {self.average_degree():.4f}"
        )

        report.append(
            f"Maximum Degree           : {self.max_degree()}"
        )

        report.append(
            f"Minimum Degree           : {self.min_degree()}"
        )

        report.append("")

        #######################################################################
        # Cluster Statistics
        #######################################################################

        report.append("[CLUSTERS]")

        report.append(
            f"Clusters                 : {self.cluster_count()}"
        )

        report.append(
            f"Largest Cluster          : {self.largest_cluster()}"
        )

        report.append(
            f"Average Cluster Size     : {self.average_cluster_size():.2f}"
        )

        report.append("")

        #######################################################################
        # Funding Statistics
        #######################################################################

        report.append("[FUNDING]")

        report.append(
            f"Average Funding Depth    : {self.average_funding_depth():.4f}"
        )

        report.append(
            f"Maximum Funding Depth    : {self.maximum_funding_depth()}"
        )

        report.append(
            f"Funding Sources          : {len(self.funding_sources())}"
        )

        report.append(
            f"Funding Destinations     : {len(self.funding_destinations())}"
        )

        report.append("")

        #######################################################################
        # Deployer Statistics
        #######################################################################

        report.append("[DEPLOYERS]")

        report.append(
            f"Deployers               : {self.deployer_count()}"
        )

        report.append(
            f"Average Launches        : {self.average_launches():.2f}"
        )

        report.append("")

        #######################################################################
        # Performance
        #######################################################################

        report.append("[PERFORMANCE]")

        report.append(
            f"Graph Memory            : {self.graph_memory():,} bytes"
        )

        report.append(
            f"Cache Memory            : {self.cache_memory():,} bytes"
        )

        report.append(
            f"Build Time              : {self.build_time():.6f} sec"
        )

        report.append(
            f"Cache Hit Rate          : {self.cache_hit_rate():.2%}"
        )

        throughput = self.throughput()

        report.append(
            f"Nodes/sec               : {throughput['nodes_per_second']:.2f}"
        )

        report.append(
            f"Edges/sec               : {throughput['edges_per_second']:.2f}"
        )

        report.append("")

        #######################################################################
        # Runtime
        #######################################################################

        report.append("[RUNTIME]")

        report.append(
            f"Errors                  : {self.total_errors}"
        )

        report.append(
            f"Last Updated            : {datetime.fromtimestamp(self.last_updated)}"
        )

        report.append(separator)

        return "\n".join(report)

    except Exception as exc:

        self.logger.exception(
            "Failed generating pretty report: %s",
            exc,
        )

        self.total_errors += 1

        return "Graph statistics unavailable."                                

