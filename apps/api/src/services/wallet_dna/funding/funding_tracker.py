# ==========================================================
# Imports
# ==========================================================

from __future__ import annotations

import json
import math
import statistics
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import (
    Any,
    Callable,
    DefaultDict,
    Deque,
    Dict,
    FrozenSet,
    Iterable,
    Iterator,
    List,
    MutableMapping,
    MutableSequence,
    Optional,
    Sequence,
    Set,
    Tuple,
    TypeAlias,
    Union,
)

import networkx as nx

# ==========================================================
# Constants
# ==========================================================

DEFAULT_LOOKUP_DEPTH = 25

DEFAULT_MAX_FUNDING_PATHS = 100

DEFAULT_CONFIDENCE = 0.50

DEFAULT_RISK_SCORE = 0.0

DEFAULT_PATH_SCORE = 0.0

DEFAULT_MIN_AMOUNT_SOL = 0.0

UNKNOWN_EXCHANGE = "Unknown Exchange"

UNKNOWN_BRIDGE = "Unknown Bridge"

UNKNOWN_FUNDER = "Unknown"

MAX_RECURSION_DEPTH = 50

DEFAULT_CACHE_SIZE = 10_000

DEFAULT_TIMEOUT_SECONDS = 30

# ==========================================================
# Enums
# ==========================================================

class FundingType(Enum):
    """
    Type of funding source.
    """

    DIRECT = "direct"

    INDIRECT = "indirect"

    EXCHANGE = "exchange"

    BRIDGE = "bridge"

    WALLET = "wallet"

    CONTRACT = "contract"

    AIRDROP = "airdrop"

    UNKNOWN = "unknown"


class FundingDirection(Enum):
    """
    Direction of capital flow.
    """

    INCOMING = "incoming"

    OUTGOING = "outgoing"

    BOTH = "both"


class FundingStatus(Enum):
    """
    Funding lookup status.
    """

    FOUND = "found"

    PARTIAL = "partial"

    NOT_FOUND = "not_found"

    UNKNOWN = "unknown"


class FundingRisk(Enum):
    """
    Risk classification.
    """

    LOW = "low"

    MEDIUM = "medium"

    HIGH = "high"

    CRITICAL = "critical"


# ==========================================================
# Type Aliases
# ==========================================================

WalletAddress: TypeAlias = str

WalletId: TypeAlias = str

TransactionSignature: TypeAlias = str

ExchangeName: TypeAlias = str

BridgeName: TypeAlias = str

FundingScore: TypeAlias = float

Confidence: TypeAlias = float

RiskScore: TypeAlias = float

Timestamp: TypeAlias = datetime

AmountSOL: TypeAlias = float

AmountUSD: TypeAlias = float

FundingPathId: TypeAlias = str

Attributes: TypeAlias = Dict[str, Any]

FundingPathList: TypeAlias = List["FundingPath"]

WalletSet: TypeAlias = Set[WalletAddress]

WalletList: TypeAlias = List[WalletAddress]

FundingGraph: TypeAlias = nx.DiGraph

FundingCache: TypeAlias = Dict[
    Tuple[WalletAddress, WalletAddress],
    Any,
]

FundingStatistics: TypeAlias = Dict[str, Any]

# ==========================================================
# Models
# ==========================================================

@dataclass(slots=True)
class FundingSource:
    """
    Represents a single funding source for a wallet.
    """

    wallet: WalletAddress

    funding_type: FundingType = FundingType.UNKNOWN

    amount_sol: AmountSOL = 0.0

    amount_usd: AmountUSD = 0.0

    tx_signature: Optional[
        TransactionSignature
    ] = None

    timestamp: Timestamp = field(
        default_factory=datetime.utcnow
    )

    exchange: Optional[
        ExchangeName
    ] = None

    bridge: Optional[
        BridgeName
    ] = None

    confidence: Confidence = DEFAULT_CONFIDENCE

    risk_score: RiskScore = DEFAULT_RISK_SCORE

    metadata: Attributes = field(
        default_factory=dict
    )

    def to_dict(self) -> Dict[str, Any]:

        return {
            "wallet": self.wallet,
            "funding_type": self.funding_type.value,
            "amount_sol": self.amount_sol,
            "amount_usd": self.amount_usd,
            "tx_signature": self.tx_signature,
            "timestamp": self.timestamp.isoformat(),
            "exchange": self.exchange,
            "bridge": self.bridge,
            "confidence": self.confidence,
            "risk_score": self.risk_score,
            "metadata": self.metadata,
        }


# ==========================================================


@dataclass(slots=True)
class FundingPath:
    """
    Represents one funding chain.
    """

    id: FundingPathId

    wallets: WalletList

    funding_type: FundingType

    total_amount_sol: AmountSOL = 0.0

    total_amount_usd: AmountUSD = 0.0

    depth: int = 0

    confidence: Confidence = DEFAULT_CONFIDENCE

    score: FundingScore = DEFAULT_PATH_SCORE

    metadata: Attributes = field(
        default_factory=dict
    )

    @property
    def source_wallet(self) -> WalletAddress:

        return self.wallets[0]

    @property
    def destination_wallet(self) -> WalletAddress:

        return self.wallets[-1]

    def to_dict(self) -> Dict[str, Any]:

        return {
            "id": self.id,
            "wallets": self.wallets,
            "funding_type": self.funding_type.value,
            "total_amount_sol": self.total_amount_sol,
            "total_amount_usd": self.total_amount_usd,
            "depth": self.depth,
            "confidence": self.confidence,
            "score": self.score,
            "metadata": self.metadata,
        }


# ==========================================================


@dataclass(slots=True)
class FundingResult:
    """
    Result produced by the FundingTracker.
    """

    wallet: WalletAddress

    status: FundingStatus = FundingStatus.UNKNOWN

    initial_funder: Optional[
        WalletAddress
    ] = None

    funding_sources: List[
        FundingSource
    ] = field(default_factory=list)

    funding_paths: FundingPathList = field(
        default_factory=list
    )

    confidence: Confidence = DEFAULT_CONFIDENCE

    risk_score: RiskScore = DEFAULT_RISK_SCORE

    metadata: Attributes = field(
        default_factory=dict
    )

    @property
    def path_count(self) -> int:

        return len(self.funding_paths)

    @property
    def source_count(self) -> int:

        return len(self.funding_sources)

    def to_dict(self) -> Dict[str, Any]:

        return {
            "wallet": self.wallet,
            "status": self.status.value,
            "initial_funder": self.initial_funder,
            "funding_sources": [
                s.to_dict()
                for s in self.funding_sources
            ],
            "funding_paths": [
                p.to_dict()
                for p in self.funding_paths
            ],
            "confidence": self.confidence,
            "risk_score": self.risk_score,
            "metadata": self.metadata,
        }


# ==========================================================


@dataclass(slots=True)
class FundingTrackerConfig:
    """
    Configuration for FundingTracker.
    """

    lookup_depth: int = DEFAULT_LOOKUP_DEPTH

    max_funding_paths: int = (
        DEFAULT_MAX_FUNDING_PATHS
    )

    recursion_limit: int = (
        MAX_RECURSION_DEPTH
    )

    min_amount_sol: AmountSOL = (
        DEFAULT_MIN_AMOUNT_SOL
    )

    confidence_threshold: Confidence = 0.50

    risk_threshold: RiskScore = 0.70

    cache_results: bool = True

    use_cache: bool = True

    cache_size: int = DEFAULT_CACHE_SIZE

    timeout_seconds: int = (
        DEFAULT_TIMEOUT_SECONDS
    )

    detect_exchanges: bool = True

    detect_bridges: bool = True

    recursive_lookup: bool = True

    allow_unknown_funders: bool = True

    metadata: Attributes = field(
        default_factory=dict
    )

# ==========================================================
# FundingTracker
# ==========================================================

class FundingTracker:
    """
    Wallet funding intelligence engine.

    Responsibilities
    ----------------
    • Initial funding discovery
    • Recursive funding lookup
    • Funding chain reconstruction
    • Exchange detection
    • Bridge detection
    • Funding similarity
    • Funding risk scoring
    • Funding reports
    """

    # ======================================================
    # Initialization
    # ======================================================

    def __init__(
        self,
        graph: Optional[FundingGraph] = None,
        config: Optional[
            FundingTrackerConfig
        ] = None,
    ) -> None:

        self.config = (
            config
            or FundingTrackerConfig()
        )

        self.graph: FundingGraph = (
            graph
            or nx.DiGraph()
        )

        # ==================================================
        # Internal Storage
        # ==================================================

        self.wallets: Dict[
            WalletAddress,
            FundingResult,
        ] = {}

        self.sources: Dict[
            WalletAddress,
            List[FundingSource],
        ] = defaultdict(list)

        self.paths: Dict[
            WalletAddress,
            FundingPathList,
        ] = defaultdict(list)

        self.exchange_wallets: Dict[
            WalletAddress,
            ExchangeName,
        ] = {}

        self.bridge_wallets: Dict[
            WalletAddress,
            BridgeName,
        ] = {}

        self.funding_graph: FundingGraph = (
            nx.DiGraph()
        )

        self.lookup_history: Dict[
            WalletAddress,
            List[WalletAddress],
        ] = defaultdict(list)

        # ==================================================
        # Cache
        # ==================================================

        self.result_cache: Dict[
            WalletAddress,
            FundingResult,
        ] = {}

        self.path_cache: Dict[
            Tuple[
                WalletAddress,
                WalletAddress,
            ],
            FundingPathList,
        ] = {}

        self.recursive_cache: Dict[
            WalletAddress,
            WalletList,
        ] = {}

        self.exchange_cache: Dict[
            WalletAddress,
            bool,
        ] = {}

        self.bridge_cache: Dict[
            WalletAddress,
            bool,
        ] = {}

        self.similarity_cache: Dict[
            Tuple[
                WalletAddress,
                WalletAddress,
            ],
            FundingScore,
        ] = {}

        # ==================================================
        # Statistics
        # ==================================================

        self.statistics: FundingStatistics = {

            "wallets_analyzed": 0,

            "funding_paths": 0,

            "sources_detected": 0,

            "exchange_wallets": 0,

            "bridge_wallets": 0,

            "recursive_lookups": 0,

            "cache_hits": 0,

            "cache_misses": 0,

            "analysis_runs": 0,

            "last_analysis": None,

            "graph_nodes": 0,

            "graph_edges": 0,

        }

# ==========================================================
# Part 2
# Initial Funding Discovery
# ==========================================================

def initial_funding_transaction(
    self,
    wallet: WalletAddress,
) -> Optional[GraphEdge]:
    """
    Return the earliest incoming funding transaction
    for a wallet.
    """

    incoming: List[GraphEdge] = []

    for _, _, edge in self.funding_graph.in_edges(
        wallet,
        data="edge",
    ):

        if edge is None:
            continue

        incoming.append(edge)

    if not incoming:
        return None

    incoming.sort(
        key=lambda e: e.block_time,
    )

    return incoming[0]


def initial_funding_wallet(
    self,
    wallet: WalletAddress,
) -> Optional[WalletAddress]:
    """
    Return the wallet responsible for the very first
    funding transaction.
    """

    tx = self.initial_funding_transaction(
        wallet,
    )

    if tx is None:
        return None

    return tx.source


def find_initial_funder(
    self,
    wallet: WalletAddress,
) -> Optional[FundingSource]:
    """
    Discover the initial funding source for a wallet.

    Produces a FundingSource model.
    """

    tx = self.initial_funding_transaction(
        wallet,
    )

    if tx is None:
        return None

    funding_type = FundingType.WALLET

    exchange = None
    bridge = None

    if self.is_exchange_wallet(
        tx.source,
    ):

        funding_type = FundingType.EXCHANGE

        exchange = self.exchange_name(
            tx.source,
        )

    elif self.is_bridge_wallet(
        tx.source,
    ):

        funding_type = FundingType.BRIDGE

        bridge = self.bridge_name(
            tx.source,
        )

    source = FundingSource(
        wallet=tx.source,
        funding_type=funding_type,
        amount_sol=tx.amount_sol,
        amount_usd=tx.amount_usd,
        tx_signature=tx.tx_signature,
        timestamp=tx.block_time,
        exchange=exchange,
        bridge=bridge,
        confidence=0.95,
        risk_score=0.0,
        metadata={
            "recipient": wallet,
            "edge_id": tx.id,
        },
    )

    self.sources[
        wallet
    ].append(source)

    self.statistics[
        "sources_detected"
    ] += 1

    return source            

# ==========================================================
# Part 3
# Funding Chains
# ==========================================================

def funding_chain(
    self,
    wallet: WalletAddress,
) -> FundingPathList:
    """
    Return all direct funding paths leading to a wallet.
    """

    if (
        self.config.use_cache
        and wallet in self.path_cache
    ):
        self.statistics["cache_hits"] += 1
        return self.path_cache[wallet]

    self.statistics["cache_misses"] += 1

    paths: FundingPathList = []

    incoming = list(
        self.funding_graph.in_edges(
            wallet,
            data="edge",
        )
    )

    incoming.sort(
        key=lambda item: (
            item[2].block_time
            if item[2] is not None
            else datetime.max
        )
    )

    for source, target, edge in incoming:

        if edge is None:
            continue

        funding_type = FundingType.WALLET

        if self.is_exchange_wallet(source):
            funding_type = FundingType.EXCHANGE

        elif self.is_bridge_wallet(source):
            funding_type = FundingType.BRIDGE

        path = FundingPath(
            id=f"{source}->{target}",
            wallets=[source, target],
            funding_type=funding_type,
            total_amount_sol=edge.amount_sol,
            total_amount_usd=edge.amount_usd,
            depth=1,
            confidence=0.95,
            score=1.0,
            metadata={
                "tx_signature": edge.tx_signature,
                "timestamp": edge.block_time.isoformat(),
            },
        )

        paths.append(path)

    if self.config.cache_results:
        self.path_cache[wallet] = paths

    return paths


# ==========================================================


def recursive_funding_chain(
    self,
    wallet: WalletAddress,
    *,
    depth: int = 0,
    visited: Optional[
        WalletSet
    ] = None,
) -> FundingPathList:
    """
    Recursively reconstruct funding paths until:

    • Exchange
    • Bridge
    • Unknown source
    • Max depth
    """

    if visited is None:
        visited = set()

    if wallet in visited:
        return []

    if depth >= self.config.lookup_depth:
        return []

    visited.add(wallet)

    chains: FundingPathList = []

    direct_paths = self.funding_chain(
        wallet,
    )

    for path in direct_paths:

        chains.append(path)

        source = path.source_wallet

        if (
            self.is_exchange_wallet(source)
            or self.is_bridge_wallet(source)
        ):
            continue

        parent_paths = self.recursive_funding_chain(
            source,
            depth=depth + 1,
            visited=visited.copy(),
        )

        for parent in parent_paths:

            merged = FundingPath(
                id=f"{parent.id}->{wallet}",
                wallets=(
                    parent.wallets
                    + [wallet]
                ),
                funding_type=parent.funding_type,
                total_amount_sol=(
                    parent.total_amount_sol
                    + path.total_amount_sol
                ),
                total_amount_usd=(
                    parent.total_amount_usd
                    + path.total_amount_usd
                ),
                depth=parent.depth + 1,
                confidence=min(
                    parent.confidence,
                    path.confidence,
                ),
                score=(
                    parent.score
                    * path.score
                ),
                metadata={
                    "recursive": True,
                },
            )

            chains.append(merged)

    return chains


# ==========================================================


def build_funding_graph(
    self,
) -> FundingGraph:
    """
    Construct a directed funding graph from all
    discovered funding paths.
    """

    graph = nx.DiGraph()

    for wallet in self.wallets:

        paths = self.recursive_funding_chain(
            wallet,
        )

        for path in paths:

            wallets = path.wallets

            for i in range(
                len(wallets) - 1
            ):

                source = wallets[i]
                target = wallets[i + 1]

                graph.add_node(source)
                graph.add_node(target)

                graph.add_edge(
                    source,
                    target,
                    funding_type=path.funding_type.value,
                    score=path.score,
                    confidence=path.confidence,
                    amount_sol=path.total_amount_sol,
                    amount_usd=path.total_amount_usd,
                )

    self.funding_graph = graph

    self.statistics[
        "graph_nodes"
    ] = graph.number_of_nodes()

    self.statistics[
        "graph_edges"
    ] = graph.number_of_edges()

    self.statistics[
        "funding_paths"
    ] = sum(
        len(
            self.recursive_funding_chain(
                wallet
            )
        )
        for wallet in self.wallets
    )

    return graph    

# ==========================================================
# Part 4
# Exchange Detection
# ==========================================================

def is_exchange_wallet(
    self,
    wallet: WalletAddress,
) -> bool:
    """
    Determine whether a wallet belongs to a known
    centralized exchange.

    Cache is checked first.
    """

    if (
        self.config.use_cache
        and wallet in self.exchange_cache
    ):
        self.statistics["cache_hits"] += 1
        return self.exchange_cache[wallet]

    self.statistics["cache_misses"] += 1

    is_exchange = wallet in self.exchange_wallets

    if self.config.cache_results:
        self.exchange_cache[
            wallet
        ] = is_exchange

    return is_exchange


# ==========================================================


def exchange_name(
    self,
    wallet: WalletAddress,
) -> ExchangeName:
    """
    Return the exchange name associated with a wallet.
    """

    return self.exchange_wallets.get(
        wallet,
        UNKNOWN_EXCHANGE,
    )


# ==========================================================


def exchange_funding(
    self,
    wallet: WalletAddress,
) -> Optional[FundingSource]:
    """
    Return the first exchange funding source for a wallet.

    Returns
    -------
    FundingSource | None
    """

    tx = self.initial_funding_transaction(
        wallet,
    )

    if tx is None:
        return None

    if not self.is_exchange_wallet(
        tx.source,
    ):
        return None

    exchange = self.exchange_name(
        tx.source,
    )

    source = FundingSource(
        wallet=tx.source,
        funding_type=FundingType.EXCHANGE,
        amount_sol=tx.amount_sol,
        amount_usd=tx.amount_usd,
        tx_signature=tx.tx_signature,
        timestamp=tx.block_time,
        exchange=exchange,
        confidence=0.99,
        risk_score=0.05,
        metadata={
            "recipient": wallet,
            "exchange_wallet": True,
            "exchange_name": exchange,
            "edge_id": tx.id,
        },
    )

    self.sources[
        wallet
    ].append(source)

    self.statistics[
        "exchange_wallets"
    ] += 1

    return source

# ==========================================================
# Part 5
# Bridge Detection
# ==========================================================

def is_bridge_wallet(
    self,
    wallet: WalletAddress,
) -> bool:
    """
    Determine whether a wallet belongs to a known
    blockchain bridge.

    Cache is checked first.
    """

    if (
        self.config.use_cache
        and wallet in self.bridge_cache
    ):
        self.statistics["cache_hits"] += 1
        return self.bridge_cache[wallet]

    self.statistics["cache_misses"] += 1

    is_bridge = wallet in self.bridge_wallets

    if self.config.cache_results:
        self.bridge_cache[
            wallet
        ] = is_bridge

    return is_bridge


# ==========================================================


def bridge_name(
    self,
    wallet: WalletAddress,
) -> BridgeName:
    """
    Return the bridge name associated with a wallet.

    Examples:
        • Wormhole
        • deBridge
        • Allbridge
        • Portal
        • LayerZero
    """

    return self.bridge_wallets.get(
        wallet,
        UNKNOWN_BRIDGE,
    )


# ==========================================================


def bridge_funding(
    self,
    wallet: WalletAddress,
) -> Optional[FundingSource]:
    """
    Return the earliest bridge funding source
    for a wallet.

    Returns
    -------
    FundingSource | None
    """

    tx = self.initial_funding_transaction(
        wallet,
    )

    if tx is None:
        return None

    if not self.is_bridge_wallet(
        tx.source,
    ):
        return None

    bridge = self.bridge_name(
        tx.source,
    )

    source = FundingSource(
        wallet=tx.source,
        funding_type=FundingType.BRIDGE,
        amount_sol=tx.amount_sol,
        amount_usd=tx.amount_usd,
        tx_signature=tx.tx_signature,
        timestamp=tx.block_time,
        bridge=bridge,
        confidence=0.99,
        risk_score=0.10,
        metadata={
            "recipient": wallet,
            "bridge_wallet": True,
            "bridge_name": bridge,
            "edge_id": tx.id,
        },
    )

    self.sources[
        wallet
    ].append(source)

    self.statistics[
        "bridge_wallets"
    ] += 1

    return source

# ==========================================================
# Part 6
# Cross Wallet Funding
# ==========================================================

def funding_paths(
    self,
    source_wallet: WalletAddress,
    destination_wallet: WalletAddress,
    *,
    max_depth: Optional[int] = None,
) -> FundingPathList:
    """
    Find all funding paths between two wallets.
    """

    if max_depth is None:
        max_depth = self.config.lookup_depth

    cache_key = (
        source_wallet,
        destination_wallet,
    )

    if (
        self.config.use_cache
        and cache_key in self.path_cache
    ):
        self.statistics["cache_hits"] += 1
        return self.path_cache[cache_key]

    self.statistics["cache_misses"] += 1

    paths: FundingPathList = []

    try:

        nx_paths = nx.all_simple_paths(
            self.funding_graph,
            source=source_wallet,
            target=destination_wallet,
            cutoff=max_depth,
        )

        for index, wallet_path in enumerate(nx_paths):

            amount_sol = 0.0
            amount_usd = 0.0
            confidence = 1.0

            for i in range(len(wallet_path) - 1):

                edge = self.funding_graph.get_edge_data(
                    wallet_path[i],
                    wallet_path[i + 1],
                    default={},
                )

                amount_sol += edge.get(
                    "amount_sol",
                    0.0,
                )

                amount_usd += edge.get(
                    "amount_usd",
                    0.0,
                )

                confidence = min(
                    confidence,
                    edge.get(
                        "confidence",
                        1.0,
                    ),
                )

            paths.append(
                FundingPath(
                    id=f"path_{index}",
                    wallets=list(wallet_path),
                    funding_type=FundingType.DIRECT,
                    total_amount_sol=amount_sol,
                    total_amount_usd=amount_usd,
                    depth=len(wallet_path) - 1,
                    confidence=confidence,
                    score=confidence,
                )
            )

    except (
        nx.NetworkXNoPath,
        nx.NodeNotFound,
    ):
        pass

    if self.config.cache_results:
        self.path_cache[
            cache_key
        ] = paths

    return paths


# ==========================================================


def common_funders(
    self,
    wallet_a: WalletAddress,
    wallet_b: WalletAddress,
) -> WalletSet:
    """
    Return wallets that have funded both wallets.
    """

    funders_a = {
        source
        for source, _, _ in self.funding_graph.in_edges(
            wallet_a,
            data=True,
        )
    }

    funders_b = {
        source
        for source, _, _ in self.funding_graph.in_edges(
            wallet_b,
            data=True,
        )
    }

    return funders_a & funders_b


# ==========================================================


def shared_funding_paths(
    self,
    wallet_a: WalletAddress,
    wallet_b: WalletAddress,
) -> FundingPathList:
    """
    Find funding paths originating from the same
    funding wallet.
    """

    shared_paths: FundingPathList = []

    funders = self.common_funders(
        wallet_a,
        wallet_b,
    )

    for funder in funders:

        paths_a = self.funding_paths(
            funder,
            wallet_a,
        )

        paths_b = self.funding_paths(
            funder,
            wallet_b,
        )

        shared_paths.extend(paths_a)
        shared_paths.extend(paths_b)

    return shared_paths

# ==========================================================
# Part 7
# Recursive Funding Lookup
# ==========================================================

def recursive_lookup(
    self,
    wallet: WalletAddress,
    *,
    max_depth: Optional[int] = None,
    stop_at: Optional[FundingType] = None,
    visited: Optional[WalletSet] = None,
) -> FundingPathList:
    """
    Recursively trace funding backwards.

    Stops when:
        • Exchange
        • Bridge
        • Unknown wallet
        • Maximum depth
    """

    if max_depth is None:
        max_depth = self.config.lookup_depth

    if visited is None:
        visited = set()

    if wallet in visited:
        return []

    if max_depth <= 0:
        return []

    visited.add(wallet)

    paths: FundingPathList = []

    incoming = list(
        self.funding_graph.in_edges(
            wallet,
            data="edge",
        )
    )

    for source, _, edge in incoming:

        if edge is None:
            continue

        funding_type = FundingType.WALLET

        if self.is_exchange_wallet(source):
            funding_type = FundingType.EXCHANGE

        elif self.is_bridge_wallet(source):
            funding_type = FundingType.BRIDGE

        path = FundingPath(
            id=f"{source}->{wallet}",
            wallets=[source, wallet],
            funding_type=funding_type,
            total_amount_sol=edge.amount_sol,
            total_amount_usd=edge.amount_usd,
            depth=1,
            confidence=edge.confidence,
            score=edge.confidence,
            metadata={
                "recursive": True,
            },
        )

        paths.append(path)

        if (
            stop_at is not None
            and funding_type == stop_at
        ):
            continue

        if funding_type == FundingType.WALLET:

            parent_paths = self.recursive_lookup(
                source,
                max_depth=max_depth - 1,
                stop_at=stop_at,
                visited=visited.copy(),
            )

            for parent in parent_paths:

                merged = FundingPath(
                    id=f"{parent.id}->{wallet}",
                    wallets=parent.wallets + [wallet],
                    funding_type=parent.funding_type,
                    total_amount_sol=(
                        parent.total_amount_sol
                        + edge.amount_sol
                    ),
                    total_amount_usd=(
                        parent.total_amount_usd
                        + edge.amount_usd
                    ),
                    depth=parent.depth + 1,
                    confidence=min(
                        parent.confidence,
                        edge.confidence,
                    ),
                    score=(
                        parent.score
                        * edge.confidence
                    ),
                    metadata={
                        "recursive": True,
                    },
                )

                paths.append(merged)

    self.statistics[
        "recursive_lookups"
    ] += 1

    return paths


# ==========================================================


def recursive_until_exchange(
    self,
    wallet: WalletAddress,
) -> FundingPathList:
    """
    Trace funding backwards until an exchange
    wallet is encountered.
    """

    return self.recursive_lookup(
        wallet,
        stop_at=FundingType.EXCHANGE,
    )


# ==========================================================


def recursive_until_bridge(
    self,
    wallet: WalletAddress,
) -> FundingPathList:
    """
    Trace funding backwards until a bridge wallet
    is encountered.
    """

    return self.recursive_lookup(
        wallet,
        stop_at=FundingType.BRIDGE,
    )


# ==========================================================


def recursive_until_unknown(
    self,
    wallet: WalletAddress,
) -> FundingPathList:
    """
    Trace funding backwards until there are no
    additional funding wallets.

    This reconstructs the entire known funding tree.
    """

    return self.recursive_lookup(
        wallet,
        stop_at=None,
    )

# ==========================================================
# Part 8
# Funding Intelligence
# ==========================================================

def funding_similarity(
    self,
    wallet_a: WalletAddress,
    wallet_b: WalletAddress,
) -> FundingScore:
    """
    Compute funding similarity between two wallets.
    """

    cache_key = (
        wallet_a,
        wallet_b,
    )

    if (
        self.config.use_cache
        and cache_key in self.similarity_cache
    ):
        self.statistics["cache_hits"] += 1
        return self.similarity_cache[
            cache_key
        ]

    self.statistics["cache_misses"] += 1

    common = self.common_funders(
        wallet_a,
        wallet_b,
    )

    paths = self.shared_funding_paths(
        wallet_a,
        wallet_b,
    )

    similarity = 0.0

    similarity += min(
        len(common) * 0.20,
        0.60,
    )

    similarity += min(
        len(paths) * 0.05,
        0.40,
    )

    similarity = min(
        similarity,
        1.0,
    )

    if self.config.cache_results:
        self.similarity_cache[
            cache_key
        ] = similarity

    return similarity


# ==========================================================


def funding_risk(
    self,
    wallet: WalletAddress,
) -> RiskScore:
    """
    Estimate funding risk.
    """

    score = 0.0

    source = self.find_initial_funder(
        wallet,
    )

    if source is None:
        return 0.0

    if source.funding_type == FundingType.UNKNOWN:
        score += 0.30

    if source.funding_type == FundingType.BRIDGE:
        score += 0.15

    if source.funding_type == FundingType.EXCHANGE:
        score += 0.05

    recursive = self.recursive_until_unknown(
        wallet,
    )

    if len(recursive) > 15:
        score += 0.20

    if len(recursive) > 30:
        score += 0.20

    score += min(
        len(
            self.common_funders(
                wallet,
                wallet,
            )
        )
        * 0.01,
        0.10,
    )

    return min(
        score,
        1.0,
    )


# ==========================================================


def funding_confidence(
    self,
    wallet: WalletAddress,
) -> Confidence:
    """
    Estimate confidence of funding attribution.
    """

    source = self.find_initial_funder(
        wallet,
    )

    if source is None:
        return 0.0

    confidence = source.confidence

    recursive = self.recursive_until_unknown(
        wallet,
    )

    confidence += min(
        len(recursive) * 0.01,
        0.20,
    )

    if self.is_exchange_wallet(
        source.wallet,
    ):
        confidence += 0.10

    if self.is_bridge_wallet(
        source.wallet,
    ):
        confidence += 0.05

    return min(
        confidence,
        1.0,
    )


# ==========================================================


def funding_explanation(
    self,
    wallet: WalletAddress,
) -> str:
    """
    Produce a human-readable funding explanation.
    """

    source = self.find_initial_funder(
        wallet,
    )

    if source is None:
        return (
            "No funding source could be "
            "identified."
        )

    chain = self.recursive_until_unknown(
        wallet,
    )

    explanation = (
        f"Wallet {wallet} appears to have "
        f"originated from {source.wallet}. "
        f"Funding type: "
        f"{source.funding_type.value}. "
        f"{len(chain)} funding paths were "
        f"identified with confidence "
        f"{self.funding_confidence(wallet):.2f}."
    )

    return explanation


# ==========================================================


def funding_summary(
    self,
    wallet: WalletAddress,
) -> Dict[str, Any]:
    """
    Produce an AI-friendly funding summary.
    """

    source = self.find_initial_funder(
        wallet,
    )

    recursive = self.recursive_until_unknown(
        wallet,
    )

    return {
        "wallet": wallet,
        "initial_funder": (
            source.wallet
            if source
            else None
        ),
        "funding_type": (
            source.funding_type.value
            if source
            else None
        ),
        "confidence": self.funding_confidence(
            wallet,
        ),
        "risk": self.funding_risk(
            wallet,
        ),
        "recursive_paths": len(
            recursive,
        ),
        "funding_sources": len(
            self.sources.get(
                wallet,
                [],
            )
        ),
        "explanation": self.funding_explanation(
            wallet,
        ),
    }                    