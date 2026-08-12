# ==========================================================
# Imports
# ==========================================================

from __future__ import annotations

import json
import math
import statistics
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import (
    Any,
    DefaultDict,
    Dict,
    FrozenSet,
    Iterable,
    List,
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

DEFAULT_CLUSTER_SCORE = 0.0

DEFAULT_CONFIDENCE = 0.50

DEFAULT_RISK_SCORE = 0.0

DEFAULT_MIN_CLUSTER_SIZE = 2

DEFAULT_MAX_CLUSTER_SIZE = 10_000

DEFAULT_CLUSTER_SIMILARITY = 0.75

DEFAULT_CLUSTER_DISTANCE = 3

DEFAULT_CACHE_SIZE = 10_000

DEFAULT_ANALYSIS_DEPTH = 20

DEFAULT_MAX_RESULTS = 100

DEFAULT_TIMEOUT_SECONDS = 30

# ==========================================================
# Enums
# ==========================================================

class ClusterType(Enum):
    """
    Types of wallet clusters.
    """

    WHALE = "whale"

    SMART_MONEY = "smart_money"

    WALLET_DNA = "wallet_dna"

    EXCHANGE = "exchange"

    DEPLOYER = "deployer"

    UNKNOWN = "unknown"


class ClusterStatus(Enum):
    """
    Cluster lifecycle status.
    """

    ACTIVE = "active"

    INACTIVE = "inactive"

    MERGED = "merged"

    ARCHIVED = "archived"


class ClusterRisk(Enum):
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

ClusterId: TypeAlias = str

NodeId: TypeAlias = str

Score: TypeAlias = float

Confidence: TypeAlias = float

RiskScore: TypeAlias = float

Timestamp: TypeAlias = datetime

Attributes: TypeAlias = Dict[str, Any]

WalletSet: TypeAlias = Set[WalletAddress]

WalletList: TypeAlias = List[WalletAddress]

ClusterGraph: TypeAlias = nx.Graph

ClusterCache: TypeAlias = Dict[str, Any]

ClusterStatistics: TypeAlias = Dict[str, Any]

# ==========================================================
# Cluster Node
# ==========================================================

@dataclass(slots=True)
class ClusterNode:
    """
    Represents one wallet inside a cluster.
    """

    wallet: WalletAddress

    score: Score = DEFAULT_CLUSTER_SCORE

    confidence: Confidence = DEFAULT_CONFIDENCE

    risk_score: RiskScore = DEFAULT_RISK_SCORE

    metadata: Attributes = field(
        default_factory=dict
    )

    def to_dict(self) -> Dict[str, Any]:

        return {
            "wallet": self.wallet,
            "score": self.score,
            "confidence": self.confidence,
            "risk_score": self.risk_score,
            "metadata": self.metadata,
        }


# ==========================================================
# Wallet Cluster
# ==========================================================

@dataclass(slots=True)
class WalletCluster:
    """
    Represents a detected wallet cluster.
    """

    id: ClusterId

    cluster_type: ClusterType

    wallets: List[ClusterNode] = field(
        default_factory=list
    )

    score: Score = DEFAULT_CLUSTER_SCORE

    confidence: Confidence = DEFAULT_CONFIDENCE

    risk_score: RiskScore = DEFAULT_RISK_SCORE

    created_at: Timestamp = field(
        default_factory=datetime.utcnow
    )

    updated_at: Timestamp = field(
        default_factory=datetime.utcnow
    )

    status: ClusterStatus = ClusterStatus.ACTIVE

    metadata: Attributes = field(
        default_factory=dict
    )

    @property
    def size(self) -> int:
        return len(self.wallets)

    def wallet_addresses(self) -> WalletList:
        return [
            node.wallet
            for node in self.wallets
        ]

    def to_dict(self) -> Dict[str, Any]:

        return {
            "id": self.id,
            "cluster_type": self.cluster_type.value,
            "wallets": [
                node.to_dict()
                for node in self.wallets
            ],
            "score": self.score,
            "confidence": self.confidence,
            "risk_score": self.risk_score,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "status": self.status.value,
            "metadata": self.metadata,
        }


# ==========================================================
# Cluster Result
# ==========================================================

@dataclass(slots=True)
class ClusterResult:
    """
    Result returned by ClusterEngine.
    """

    cluster: WalletCluster

    explanation: str = ""

    statistics: Attributes = field(
        default_factory=dict
    )

    recommendations: List[str] = field(
        default_factory=list
    )

    def to_dict(self) -> Dict[str, Any]:

        return {
            "cluster": self.cluster.to_dict(),
            "explanation": self.explanation,
            "statistics": self.statistics,
            "recommendations": self.recommendations,
        }


# ==========================================================
# Cluster Configuration
# ==========================================================

@dataclass(slots=True)
class ClusterConfig:
    """
    Configuration for ClusterEngine.
    """

    min_cluster_size: int = DEFAULT_MIN_CLUSTER_SIZE

    max_cluster_size: int = DEFAULT_MAX_CLUSTER_SIZE

    similarity_threshold: float = DEFAULT_CLUSTER_SIMILARITY

    graph_distance: int = DEFAULT_CLUSTER_DISTANCE

    analysis_depth: int = DEFAULT_ANALYSIS_DEPTH

    cache_size: int = DEFAULT_CACHE_SIZE

    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS

    max_results: int = DEFAULT_MAX_RESULTS

    cache_results: bool = True

    use_cache: bool = True

    enable_whale_detection: bool = True

    enable_smart_money: bool = True

    enable_wallet_dna: bool = True

    enable_exchange_clusters: bool = True

    enable_deployer_clusters: bool = True

    metadata: Attributes = field(
        default_factory=dict
    )

# ==========================================================
# Cluster Engine
# ==========================================================

class ClusterEngine:
    """
    Wallet clustering engine.

    Responsible for detecting:

    • Whale clusters
    • Smart Money clusters
    • Wallet DNA clusters
    • Exchange clusters
    • Deployer clusters
    """

    # ======================================================
    # Initialization
    # ======================================================

    def __init__(
        self,
        graph_builder=None,
        relationship_detector=None,
        funding_tracker=None,
        config: Optional[
            ClusterConfig
        ] = None,
    ) -> None:

        self.config = (
            config
            or ClusterConfig()
        )

        self.graph_builder = graph_builder

        self.relationship_detector = (
            relationship_detector
        )

        self.funding_tracker = (
            funding_tracker
        )

        self.graph: ClusterGraph = (
            nx.Graph()
        )

        # ==================================================
        # Internal Storage
        # ==================================================

        self.clusters: Dict[
            ClusterId,
            WalletCluster,
        ] = {}

        self.cluster_results: Dict[
            ClusterId,
            ClusterResult,
        ] = {}

        self.wallet_to_cluster: Dict[
            WalletAddress,
            ClusterId,
        ] = {}

        self.cluster_graph: ClusterGraph = (
            nx.Graph()
        )

        self.whale_clusters: Set[
            ClusterId
        ] = set()

        self.smart_money_clusters: Set[
            ClusterId
        ] = set()

        self.wallet_dna_clusters: Set[
            ClusterId
        ] = set()

        self.exchange_clusters: Set[
            ClusterId
        ] = set()

        self.deployer_clusters: Set[
            ClusterId
        ] = set()

        # ==================================================
        # Cache
        # ==================================================

        self.cluster_cache: Dict[
            ClusterId,
            WalletCluster,
        ] = {}

        self.wallet_cache: Dict[
            WalletAddress,
            ClusterId,
        ] = {}

        self.similarity_cache: Dict[
            Tuple[
                WalletAddress,
                WalletAddress,
            ],
            float,
        ] = {}

        self.score_cache: Dict[
            WalletAddress,
            float,
        ] = {}

        self.result_cache: Dict[
            ClusterId,
            ClusterResult,
        ] = {}

        # ==================================================
        # Statistics
        # ==================================================

        self.statistics: ClusterStatistics = {

            "analysis_runs": 0,

            "clusters": 0,

            "wallets": 0,

            "whale_clusters": 0,

            "smart_money_clusters": 0,

            "wallet_dna_clusters": 0,

            "exchange_clusters": 0,

            "deployer_clusters": 0,

            "cache_hits": 0,

            "cache_misses": 0,

            "graph_nodes": 0,

            "graph_edges": 0,

            "largest_cluster": 0,

            "average_cluster_size": 0.0,

            "last_analysis": None,

        }

# ==========================================================
# Part 3
# Whale Clustering
# ==========================================================

def whale_score(
    self,
    wallet: WalletAddress,
) -> float:
    """
    Calculate a whale score for a wallet.

    Score is normalized to [0.0, 1.0].
    """

    if wallet in self.score_cache:

        self.statistics["cache_hits"] += 1

        return self.score_cache[
            wallet
        ]

    self.statistics["cache_misses"] += 1

    score = 0.0

    # --------------------------------------------------
    # Wallet metadata
    # --------------------------------------------------

    node = None

    if (
        self.graph_builder is not None
        and hasattr(
            self.graph_builder,
            "get_node_by_address",
        )
    ):

        node = (
            self.graph_builder
            .get_node_by_address(
                wallet
            )
        )

    if node is not None:

        # SOL balance
        score += min(
            node.balance_sol
            / 1000.0,
            0.35,
        )

        # USD value
        score += min(
            node.usd_value
            / 1_000_000.0,
            0.30,
        )

        # Activity
        score += min(
            node.tx_count
            / 5000.0,
            0.15,
        )

        # Token diversity
        score += min(
            node.token_count
            / 500.0,
            0.10,
        )

    # --------------------------------------------------
    # Funding intelligence
    # --------------------------------------------------

    if self.funding_tracker is not None:

        confidence = (
            self.funding_tracker
            .funding_confidence(
                wallet
            )
        )

        score += (
            confidence * 0.10
        )

    score = min(
        score,
        1.0,
    )

    self.score_cache[
        wallet
    ] = score

    return score


# ==========================================================


def whale_cluster_strength(
    self,
    cluster: WalletCluster,
) -> float:
    """
    Compute overall whale strength
    of a cluster.
    """

    if cluster.size == 0:
        return 0.0

    scores = [

        self.whale_score(
            node.wallet
        )

        for node in cluster.wallets

    ]

    average_score = (
        statistics.mean(
            scores
        )
    )

    size_bonus = min(
        cluster.size / 50.0,
        0.20,
    )

    confidence_bonus = (
        cluster.confidence
        * 0.10
    )

    strength = (
        average_score
        + size_bonus
        + confidence_bonus
    )

    return min(
        strength,
        1.0,
    )


# ==========================================================


def detect_whale_clusters(
    self,
    *,
    threshold: float = 0.75,
) -> List[WalletCluster]:
    """
    Detect whale clusters.

    A whale cluster consists of wallets
    whose whale score exceeds the
    specified threshold.
    """

    detected: List[
        WalletCluster
    ] = []

    wallets: WalletList = []

    if (
        self.graph_builder
        is not None
    ):

        wallets = list(
            self.graph_builder
            .address_index.keys()
        )

    for wallet in wallets:

        score = self.whale_score(
            wallet
        )

        if score < threshold:
            continue

        node = ClusterNode(
            wallet=wallet,
            score=score,
            confidence=score,
            risk_score=0.20,
        )

        cluster = WalletCluster(

            id=f"whale_{wallet}",

            cluster_type=ClusterType.WHALE,

            wallets=[node],

            score=score,

            confidence=score,

            risk_score=0.20,

        )

        strength = (
            self.whale_cluster_strength(
                cluster
            )
        )

        cluster.score = strength

        self.clusters[
            cluster.id
        ] = cluster

        self.wallet_to_cluster[
            wallet
        ] = cluster.id

        self.whale_clusters.add(
            cluster.id
        )

        detected.append(
            cluster
        )

    # ----------------------------------------------

    self.statistics[
        "clusters"
    ] = len(
        self.clusters
    )

    self.statistics[
        "whale_clusters"
    ] = len(
        self.whale_clusters
    )

    if detected:

        self.statistics[
            "largest_cluster"
        ] = max(
            c.size
            for c in detected
        )

        self.statistics[
            "average_cluster_size"
        ] = statistics.mean(
            c.size
            for c in detected
        )

    return detected

# ==========================================================
# Part 4
# Smart Money Clustering
# ==========================================================

def smart_money_score(
    self,
    wallet: WalletAddress,
) -> float:
    """
    Calculate a Smart Money score.

    Score range:
        0.0 → 1.0
    """

    cache_key = (
        "smart_money",
        wallet,
    )

    if cache_key in self.score_cache:

        self.statistics["cache_hits"] += 1

        return self.score_cache[
            cache_key
        ]

    self.statistics["cache_misses"] += 1

    score = 0.0

    node = None

    if (
        self.graph_builder
        and hasattr(
            self.graph_builder,
            "get_node_by_address",
        )
    ):

        node = (
            self.graph_builder
            .get_node_by_address(
                wallet
            )
        )

    # --------------------------------------------------
    # Wallet activity
    # --------------------------------------------------

    if node is not None:

        score += min(
            node.tx_count / 10000,
            0.20,
        )

        score += min(
            node.token_count / 300,
            0.15,
        )

        score += min(
            node.balance_sol / 500,
            0.15,
        )

    # --------------------------------------------------
    # Funding intelligence
    # --------------------------------------------------

    if self.funding_tracker:

        score += (
            self.funding_tracker
            .funding_confidence(
                wallet
            )
            * 0.20
        )

    # --------------------------------------------------
    # Relationship intelligence
    # --------------------------------------------------

    if (
        self.relationship_detector
        and hasattr(
            self.relationship_detector,
            "wallet_clusters",
        )
    ):

        for cluster in (
            self.relationship_detector
            .wallet_clusters
        ):

            if wallet in cluster:

                score += 0.20

                break

    # --------------------------------------------------
    # Graph connectivity
    # --------------------------------------------------

    if wallet in self.graph:

        degree = (
            self.graph.degree(
                wallet
            )
        )

        score += min(
            degree / 50,
            0.10,
        )

    score = min(
        score,
        1.0,
    )

    self.score_cache[
        cache_key
    ] = score

    return score


# ==========================================================


def smart_money_confidence(
    self,
    wallet: WalletAddress,
) -> float:
    """
    Confidence that the wallet belongs to
    Smart Money.
    """

    confidence = (
        self.smart_money_score(
            wallet
        )
    )

    if self.funding_tracker:

        confidence += (
            self.funding_tracker
            .funding_confidence(
                wallet
            )
            * 0.20
        )

    if (
        self.relationship_detector
        and hasattr(
            self.relationship_detector,
            "relationship_confidence",
        )
    ):

        try:

            confidence += (
                self.relationship_detector
                .relationship_confidence(
                    wallet,
                    wallet,
                )
                * 0.10
            )

        except Exception:

            pass

    return min(
        confidence,
        1.0,
    )


# ==========================================================


def detect_smart_money_clusters(
    self,
    *,
    threshold: float = 0.70,
) -> List[WalletCluster]:
    """
    Detect Smart Money clusters.
    """

    clusters: List[
        WalletCluster
    ] = []

    wallets: WalletList = []

    if self.graph_builder:

        wallets = list(
            self.graph_builder
            .address_index.keys()
        )

    for wallet in wallets:

        score = (
            self.smart_money_score(
                wallet
            )
        )

        if score < threshold:
            continue

        confidence = (
            self.smart_money_confidence(
                wallet
            )
        )

        cluster = WalletCluster(

            id=f"smart_{wallet}",

            cluster_type=ClusterType.SMART_MONEY,

            wallets=[
                ClusterNode(
                    wallet=wallet,
                    score=score,
                    confidence=confidence,
                    risk_score=0.10,
                )
            ],

            score=score,

            confidence=confidence,

            risk_score=0.10,

        )

        self.clusters[
            cluster.id
        ] = cluster

        self.wallet_to_cluster[
            wallet
        ] = cluster.id

        self.smart_money_clusters.add(
            cluster.id
        )

        clusters.append(
            cluster
        )

    self.statistics[
        "smart_money_clusters"
    ] = len(
        self.smart_money_clusters
    )

    self.statistics[
        "clusters"
    ] = len(
        self.clusters
    )

    return clusters

# ==========================================================
# Part 5
# Wallet DNA Clustering
# ==========================================================

def wallet_similarity_cluster(
    self,
    wallet: WalletAddress,
    similarity_threshold: Optional[float] = None,
) -> WalletCluster:
    """
    Build a Wallet DNA cluster around a wallet using
    relationship and funding similarity.
    """

    if similarity_threshold is None:
        similarity_threshold = (
            self.config.similarity_threshold
        )

    cluster = WalletCluster(
        id=f"dna_{wallet}",
        cluster_type=ClusterType.WALLET_DNA,
    )

    seed_score = 1.0

    cluster.wallets.append(
        ClusterNode(
            wallet=wallet,
            score=seed_score,
            confidence=1.0,
            risk_score=0.0,
        )
    )

    wallets = []

    if self.graph_builder:

        wallets = list(
            self.graph_builder.address_index.keys()
        )

    for other in wallets:

        if other == wallet:
            continue

        similarity = 0.0

        # ----------------------------------------------
        # Relationship similarity
        # ----------------------------------------------

        if (
            self.relationship_detector
            and hasattr(
                self.relationship_detector,
                "overall_relationship_score",
            )
        ):

            try:

                similarity += (
                    self.relationship_detector
                    .overall_relationship_score(
                        wallet,
                        other,
                    )
                    * 0.60
                )

            except Exception:

                pass

        # ----------------------------------------------
        # Funding similarity
        # ----------------------------------------------

        if self.funding_tracker:

            similarity += (
                self.funding_tracker
                .funding_similarity(
                    wallet,
                    other,
                )
                * 0.40
            )

        if similarity < similarity_threshold:
            continue

        cluster.wallets.append(

            ClusterNode(

                wallet=other,

                score=similarity,

                confidence=similarity,

                risk_score=0.10,

            )

        )

    if cluster.size > 0:

        cluster.score = statistics.mean(
            node.score
            for node in cluster.wallets
        )

        cluster.confidence = statistics.mean(
            node.confidence
            for node in cluster.wallets
        )

        cluster.risk_score = statistics.mean(
            node.risk_score
            for node in cluster.wallets
        )

    return cluster


# ==========================================================


def merge_wallet_clusters(
    self,
    clusters: List[WalletCluster],
) -> List[WalletCluster]:
    """
    Merge Wallet DNA clusters sharing common wallets.
    """

    merged: List[
        WalletCluster
    ] = []

    visited: Set[
        ClusterId
    ] = set()

    for cluster in clusters:

        if cluster.id in visited:
            continue

        wallets = {
            node.wallet
            for node in cluster.wallets
        }

        merged_cluster = WalletCluster(
            id=cluster.id,
            cluster_type=ClusterType.WALLET_DNA,
        )

        for other in clusters:

            if other.id == cluster.id:
                continue

            other_wallets = {
                node.wallet
                for node in other.wallets
            }

            if wallets & other_wallets:

                wallets |= other_wallets

                visited.add(other.id)

        for wallet in wallets:

            merged_cluster.wallets.append(

                ClusterNode(
                    wallet=wallet,
                    score=1.0,
                    confidence=1.0,
                )

            )

        merged_cluster.score = statistics.mean(
            n.score
            for n in merged_cluster.wallets
        )

        merged_cluster.confidence = statistics.mean(
            n.confidence
            for n in merged_cluster.wallets
        )

        merged.append(
            merged_cluster
        )

        visited.add(cluster.id)

    return merged


# ==========================================================


def detect_wallet_dna_clusters(
    self,
) -> List[WalletCluster]:
    """
    Detect Wallet DNA clusters across the graph.
    """

    wallets = []

    if self.graph_builder:

        wallets = list(
            self.graph_builder.address_index.keys()
        )

    clusters: List[
        WalletCluster
    ] = []

    for wallet in wallets:

        cluster = (
            self.wallet_similarity_cluster(
                wallet
            )
        )

        if (
            cluster.size
            < self.config.min_cluster_size
        ):
            continue

        clusters.append(
            cluster
        )

    clusters = self.merge_wallet_clusters(
        clusters
    )

    for cluster in clusters:

        self.clusters[
            cluster.id
        ] = cluster

        self.wallet_dna_clusters.add(
            cluster.id
        )

        for node in cluster.wallets:

            self.wallet_to_cluster[
                node.wallet
            ] = cluster.id

    self.statistics[
        "wallet_dna_clusters"
    ] = len(
        self.wallet_dna_clusters
    )

    self.statistics[
        "clusters"
    ] = len(
        self.clusters
    )

    return clusters

# ==========================================================
# Part 6
# Exchange Clustering
# ==========================================================

def exchange_members(
    self,
    exchange: Union[
        ExchangeName,
        WalletAddress,
    ],
) -> WalletList:
    """
    Return all wallets belonging to a given exchange.

    The input may be:
        • Exchange name
        • Exchange wallet
    """

    members: WalletList = []

    if self.funding_tracker is None:
        return members

    # ----------------------------------------------
    # Determine exchange name
    # ----------------------------------------------

    if self.funding_tracker.is_exchange_wallet(
        exchange
    ):
        exchange = (
            self.funding_tracker
            .exchange_name(exchange)
        )

    # ----------------------------------------------

    for (
        wallet,
        exchange_name,
    ) in (
        self.funding_tracker
        .exchange_wallets.items()
    ):

        if exchange_name == exchange:

            members.append(wallet)

    return members


# ==========================================================


def exchange_cluster_score(
    self,
    wallets: WalletList,
) -> float:
    """
    Compute an aggregate score for an exchange cluster.
    """

    if not wallets:
        return 0.0

    scores: List[float] = []

    for wallet in wallets:

        score = 0.0

        # ------------------------------------------
        # Whale influence
        # ------------------------------------------

        score += (
            self.whale_score(wallet)
            * 0.40
        )

        # ------------------------------------------
        # Smart Money influence
        # ------------------------------------------

        score += (
            self.smart_money_score(
                wallet
            )
            * 0.20
        )

        # ------------------------------------------
        # Funding confidence
        # ------------------------------------------

        if self.funding_tracker:

            score += (
                self.funding_tracker
                .funding_confidence(
                    wallet
                )
                * 0.40
            )

        scores.append(score)

    return min(
        statistics.mean(scores),
        1.0,
    )


# ==========================================================


def detect_exchange_clusters(
    self,
) -> List[WalletCluster]:
    """
    Detect clusters of wallets belonging to the
    same centralized exchange.
    """

    if self.funding_tracker is None:
        return []

    grouped: DefaultDict[
        ExchangeName,
        WalletList,
    ] = defaultdict(list)

    # ----------------------------------------------
    # Group wallets by exchange
    # ----------------------------------------------

    for (
        wallet,
        exchange,
    ) in (
        self.funding_tracker
        .exchange_wallets.items()
    ):

        grouped[
            exchange
        ].append(wallet)

    detected: List[
        WalletCluster
    ] = []

    # ----------------------------------------------
    # Create clusters
    # ----------------------------------------------

    for (
        exchange,
        wallets,
    ) in grouped.items():

        cluster = WalletCluster(

            id=f"exchange_{exchange}",

            cluster_type=ClusterType.EXCHANGE,

            metadata={
                "exchange": exchange,
            },

        )

        for wallet in wallets:

            confidence = 1.0

            if self.funding_tracker:

                confidence = (
                    self.funding_tracker
                    .funding_confidence(
                        wallet
                    )
                )

            cluster.wallets.append(

                ClusterNode(

                    wallet=wallet,

                    score=self.whale_score(
                        wallet
                    ),

                    confidence=confidence,

                    risk_score=0.05,

                )

            )

        cluster.score = (
            self.exchange_cluster_score(
                wallets
            )
        )

        cluster.confidence = statistics.mean(
            node.confidence
            for node in cluster.wallets
        )

        cluster.risk_score = 0.05

        self.clusters[
            cluster.id
        ] = cluster

        self.exchange_clusters.add(
            cluster.id
        )

        for node in cluster.wallets:

            self.wallet_to_cluster[
                node.wallet
            ] = cluster.id

        detected.append(cluster)

    # ----------------------------------------------

    self.statistics[
        "exchange_clusters"
    ] = len(
        self.exchange_clusters
    )

    self.statistics[
        "clusters"
    ] = len(
        self.clusters
    )

    return detected

# ==========================================================
# Part 7
# Deployer Clustering
# ==========================================================

def deployer_members(
    self,
    deployer: WalletAddress,
) -> WalletList:
    """
    Return all wallets belonging to a deployer cluster.

    A wallet belongs to the cluster if it has the
    same deployer.
    """

    members: WalletList = []

    if (
        self.relationship_detector is None
        or not hasattr(
            self.relationship_detector,
            "related_deployer_wallets",
        )
    ):
        return members

    try:

        members = list(
            self.relationship_detector
            .related_deployer_wallets(
                deployer
            )
        )

    except Exception:

        return []

    if deployer not in members:
        members.insert(
            0,
            deployer,
        )

    return list(dict.fromkeys(members))


# ==========================================================


def deployer_cluster_score(
    self,
    wallets: WalletList,
) -> float:
    """
    Calculate an overall deployer cluster score.
    """

    if not wallets:
        return 0.0

    scores: List[float] = []

    for wallet in wallets:

        score = 0.0

        # ------------------------------------------
        # Whale influence
        # ------------------------------------------

        score += (
            self.whale_score(wallet)
            * 0.25
        )

        # ------------------------------------------
        # Smart Money influence
        # ------------------------------------------

        score += (
            self.smart_money_score(
                wallet
            )
            * 0.20
        )

        # ------------------------------------------
        # Funding confidence
        # ------------------------------------------

        if self.funding_tracker:

            score += (
                self.funding_tracker
                .funding_confidence(
                    wallet
                )
                * 0.25
            )

        # ------------------------------------------
        # Deployer similarity
        # ------------------------------------------

        if (
            self.relationship_detector
            and hasattr(
                self.relationship_detector,
                "deployer_similarity",
            )
        ):

            try:

                score += (
                    self.relationship_detector
                    .deployer_similarity(
                        wallet,
                        wallets[0],
                    )
                    * 0.30
                )

            except Exception:

                pass

        scores.append(score)

    return min(
        statistics.mean(scores),
        1.0,
    )


# ==========================================================


def detect_deployer_clusters(
    self,
) -> List[WalletCluster]:
    """
    Detect deployer-based wallet clusters.
    """

    if self.relationship_detector is None:
        return []

    processed: Set[
        WalletAddress
    ] = set()

    clusters: List[
        WalletCluster
    ] = []

    wallets: WalletList = []

    if self.graph_builder:

        wallets = list(
            self.graph_builder
            .address_index.keys()
        )

    for wallet in wallets:

        if wallet in processed:
            continue

        members = self.deployer_members(
            wallet
        )

        if (
            len(members)
            < self.config.min_cluster_size
        ):
            continue

        cluster = WalletCluster(

            id=f"deployer_{wallet}",

            cluster_type=ClusterType.DEPLOYER,

            metadata={
                "deployer": wallet,
            },

        )

        for member in members:

            confidence = 1.0

            if self.funding_tracker:

                confidence = (
                    self.funding_tracker
                    .funding_confidence(
                        member
                    )
                )

            cluster.wallets.append(

                ClusterNode(

                    wallet=member,

                    score=self.whale_score(
                        member
                    ),

                    confidence=confidence,

                    risk_score=0.15,

                )

            )

            processed.add(member)

            self.wallet_to_cluster[
                member
            ] = cluster.id

        cluster.score = (
            self.deployer_cluster_score(
                members
            )
        )

        cluster.confidence = statistics.mean(
            node.confidence
            for node in cluster.wallets
        )

        cluster.risk_score = statistics.mean(
            node.risk_score
            for node in cluster.wallets
        )

        self.clusters[
            cluster.id
        ] = cluster

        self.deployer_clusters.add(
            cluster.id
        )

        clusters.append(cluster)

    self.statistics[
        "deployer_clusters"
    ] = len(
        self.deployer_clusters
    )

    self.statistics[
        "clusters"
    ] = len(
        self.clusters
    )

    return clusters                

# ==========================================================
# Part 8
# Composite Cluster Intelligence
# ==========================================================

def cluster_similarity(
    self,
    cluster_a: WalletCluster,
    cluster_b: WalletCluster,
) -> float:
    """
    Compute similarity between two clusters.

    Combines:
        • Shared wallets
        • Funding similarity
        • Relationship similarity
    """

    wallets_a = {
        node.wallet
        for node in cluster_a.wallets
    }

    wallets_b = {
        node.wallet
        for node in cluster_b.wallets
    }

    # ------------------------------------------
    # Wallet overlap (Jaccard)
    # ------------------------------------------

    intersection = wallets_a & wallets_b
    union = wallets_a | wallets_b

    wallet_similarity = (
        len(intersection) / len(union)
        if union
        else 0.0
    )

    # ------------------------------------------
    # Funding similarity
    # ------------------------------------------

    funding_similarity = 0.0

    if self.funding_tracker:

        comparisons = []

        for wa in wallets_a:
            for wb in wallets_b:

                comparisons.append(
                    self.funding_tracker
                    .funding_similarity(
                        wa,
                        wb,
                    )
                )

        if comparisons:

            funding_similarity = (
                statistics.mean(
                    comparisons
                )
            )

    # ------------------------------------------
    # Relationship similarity
    # ------------------------------------------

    relationship_similarity = 0.0

    if (
        self.relationship_detector
        and hasattr(
            self.relationship_detector,
            "overall_relationship_score",
        )
    ):

        comparisons = []

        for wa in wallets_a:
            for wb in wallets_b:

                try:

                    comparisons.append(
                        self.relationship_detector
                        .overall_relationship_score(
                            wa,
                            wb,
                        )
                    )

                except Exception:

                    pass

        if comparisons:

            relationship_similarity = (
                statistics.mean(
                    comparisons
                )
            )

    similarity = (
        wallet_similarity * 0.30
        + funding_similarity * 0.35
        + relationship_similarity * 0.35
    )

    return min(similarity, 1.0)


# ==========================================================


def cluster_confidence(
    self,
    cluster: WalletCluster,
) -> float:
    """
    Compute confidence for an entire cluster.
    """

    if cluster.size == 0:
        return 0.0

    values = [
        node.confidence
        for node in cluster.wallets
    ]

    confidence = statistics.mean(values)

    confidence *= (
        1.0 + min(cluster.size / 100, 0.15)
    )

    return min(confidence, 1.0)


# ==========================================================


def cluster_risk(
    self,
    cluster: WalletCluster,
) -> float:
    """
    Compute overall cluster risk.
    """

    if cluster.size == 0:
        return 0.0

    risk = statistics.mean(
        node.risk_score
        for node in cluster.wallets
    )

    if cluster.cluster_type == ClusterType.WHALE:
        risk += 0.05

    elif cluster.cluster_type == ClusterType.DEPLOYER:
        risk += 0.20

    elif cluster.cluster_type == ClusterType.WALLET_DNA:
        risk += 0.15

    elif cluster.cluster_type == ClusterType.EXCHANGE:
        risk += 0.02

    return min(risk, 1.0)


# ==========================================================


def explain_cluster(
    self,
    cluster: WalletCluster,
) -> str:
    """
    Generate an AI-readable explanation
    for a cluster.
    """

    return (
        f"{cluster.cluster_type.value.replace('_', ' ').title()} "
        f"cluster containing {cluster.size} wallets. "
        f"Overall score: {cluster.score:.2f}. "
        f"Confidence: {self.cluster_confidence(cluster):.2f}. "
        f"Risk: {self.cluster_risk(cluster):.2f}."
    )


# ==========================================================


def cluster_summary(
    self,
    cluster: WalletCluster,
) -> Dict[str, Any]:
    """
    Produce a structured AI summary for a cluster.
    """

    return {
        "cluster_id": cluster.id,
        "cluster_type": cluster.cluster_type.value,
        "wallet_count": cluster.size,
        "wallets": cluster.wallet_addresses(),
        "score": cluster.score,
        "confidence": self.cluster_confidence(
            cluster,
        ),
        "risk": self.cluster_risk(
            cluster,
        ),
        "status": cluster.status.value,
        "metadata": cluster.metadata,
        "explanation": self.explain_cluster(
            cluster,
        ),
    }

# ==========================================================
# Part 9
# Analytics
# ==========================================================

def largest_clusters(
    self,
    limit: int = 10,
) -> List[WalletCluster]:
    """
    Return the largest clusters ordered by
    wallet count.
    """

    return sorted(
        self.clusters.values(),
        key=lambda cluster: cluster.size,
        reverse=True,
    )[:limit]


# ==========================================================


def highest_risk_clusters(
    self,
    limit: int = 10,
) -> List[WalletCluster]:
    """
    Return clusters ordered by overall risk.
    """

    return sorted(
        self.clusters.values(),
        key=self.cluster_risk,
        reverse=True,
    )[:limit]


# ==========================================================


def top_whales(
    self,
    limit: int = 25,
) -> List[Tuple[WalletAddress, float]]:
    """
    Return the highest scoring whale wallets.
    """

    rankings: List[
        Tuple[
            WalletAddress,
            float,
        ]
    ] = []

    if self.graph_builder:

        wallets = list(
            self.graph_builder
            .address_index.keys()
        )

        for wallet in wallets:

            rankings.append(
                (
                    wallet,
                    self.whale_score(
                        wallet,
                    ),
                )
            )

    rankings.sort(
        key=lambda item: item[1],
        reverse=True,
    )

    return rankings[:limit]


# ==========================================================


def top_smart_money(
    self,
    limit: int = 25,
) -> List[Tuple[WalletAddress, float]]:
    """
    Return the highest scoring Smart Money wallets.
    """

    rankings: List[
        Tuple[
            WalletAddress,
            float,
        ]
    ] = []

    if self.graph_builder:

        wallets = list(
            self.graph_builder
            .address_index.keys()
        )

        for wallet in wallets:

            rankings.append(
                (
                    wallet,
                    self.smart_money_score(
                        wallet,
                    ),
                )
            )

    rankings.sort(
        key=lambda item: item[1],
        reverse=True,
    )

    return rankings[:limit]


# ==========================================================


def cluster_statistics(
    self,
) -> Dict[str, Any]:
    """
    Produce overall clustering statistics.
    """

    clusters = list(
        self.clusters.values()
    )

    sizes = [
        cluster.size
        for cluster in clusters
    ]

    scores = [
        cluster.score
        for cluster in clusters
    ]

    risks = [
        self.cluster_risk(cluster)
        for cluster in clusters
    ]

    confidences = [
        self.cluster_confidence(
            cluster
        )
        for cluster in clusters
    ]

    return {

        "total_clusters": len(clusters),

        "total_wallets": sum(sizes),

        "largest_cluster": (
            max(sizes)
            if sizes
            else 0
        ),

        "smallest_cluster": (
            min(sizes)
            if sizes
            else 0
        ),

        "average_cluster_size": (
            statistics.mean(sizes)
            if sizes
            else 0.0
        ),

        "median_cluster_size": (
            statistics.median(sizes)
            if sizes
            else 0.0
        ),

        "average_cluster_score": (
            statistics.mean(scores)
            if scores
            else 0.0
        ),

        "average_risk": (
            statistics.mean(risks)
            if risks
            else 0.0
        ),

        "average_confidence": (
            statistics.mean(
                confidences
            )
            if confidences
            else 0.0
        ),

        "whale_clusters": len(
            self.whale_clusters
        ),

        "smart_money_clusters": len(
            self.smart_money_clusters
        ),

        "wallet_dna_clusters": len(
            self.wallet_dna_clusters
        ),

        "exchange_clusters": len(
            self.exchange_clusters
        ),

        "deployer_clusters": len(
            self.deployer_clusters
        ),

        "cache_hits": self.statistics.get(
            "cache_hits",
            0,
        ),

        "cache_misses": self.statistics.get(
            "cache_misses",
            0,
        ),

        "analysis_runs": self.statistics.get(
            "analysis_runs",
            0,
        ),

        "last_analysis": self.statistics.get(
            "last_analysis",
        ),

    }

# ==========================================================
# Part 10
# Export
# ==========================================================

def to_dict(
    self,
) -> Dict[str, Any]:
    """
    Export the complete ClusterEngine state as a dictionary.
    """

    return {

        "clusters": {
            cluster_id: cluster.to_dict()
            for (
                cluster_id,
                cluster,
            ) in self.clusters.items()
        },

        "statistics": self.cluster_statistics(),

        "config": vars(self.config),

        "metadata": {
            "cluster_count": len(
                self.clusters
            ),
            "generated_at": datetime.utcnow().isoformat(),
            "version": "1.0",
        },

    }


# ==========================================================


def to_json(
    self,
    *,
    indent: int = 4,
) -> str:
    """
    Export ClusterEngine as JSON.
    """

    return json.dumps(
        self.to_dict(),
        indent=indent,
        default=str,
    )


# ==========================================================


def to_dataframe(
    self,
):
    """
    Export clusters as a pandas DataFrame.

    Raises:
        ImportError if pandas is unavailable.
    """

    try:

        import pandas as pd

    except ImportError as exc:

        raise ImportError(
            "pandas is required for "
            "to_dataframe()."
        ) from exc

    rows = []

    for cluster in self.clusters.values():

        for node in cluster.wallets:

            rows.append({

                "cluster_id": cluster.id,

                "cluster_type": (
                    cluster.cluster_type.value
                ),

                "wallet": node.wallet,

                "wallet_score": node.score,

                "wallet_confidence": (
                    node.confidence
                ),

                "wallet_risk": (
                    node.risk_score
                ),

                "cluster_score": (
                    cluster.score
                ),

                "cluster_confidence": (
                    cluster.confidence
                ),

                "cluster_risk": (
                    cluster.risk_score
                ),

                "cluster_size": (
                    cluster.size
                ),

                "status": (
                    cluster.status.value
                ),

            })

    return pd.DataFrame(rows)


# ==========================================================


def save_json(
    self,
    path: Union[
        str,
        Path,
    ],
    *,
    indent: int = 4,
) -> Path:
    """
    Save ClusterEngine to a JSON file.
    """

    path = Path(path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        self.to_json(
            indent=indent,
        ),
        encoding="utf-8",
    )

    return path


# ==========================================================


def to_csv(
    self,
    path: Optional[
        Union[str, Path]
    ] = None,
):
    """
    Export clusters to CSV.

    Returns:
        pandas.DataFrame if path is None.

        Otherwise saves the CSV and
        returns the output path.
    """

    df = self.to_dataframe()

    if path is None:
        return df

    path = Path(path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(
        path,
        index=False,
    )

    return path

# ==========================================================
# Part 11
# Engine
# ==========================================================

def analyze_cluster(
    self,
    cluster: WalletCluster,
) -> ClusterResult:
    """
    Analyze a single cluster and produce a
    complete ClusterResult.
    """

    cluster.score = max(
        cluster.score,
        self.cluster_similarity(cluster, cluster),
    )

    cluster.confidence = self.cluster_confidence(
        cluster,
    )

    cluster.risk_score = self.cluster_risk(
        cluster,
    )

    cluster.updated_at = datetime.utcnow()

    result = ClusterResult(
        cluster=cluster,
        explanation=self.explain_cluster(
            cluster,
        ),
        statistics={
            "wallet_count": cluster.size,
            "cluster_score": cluster.score,
            "cluster_confidence": (
                cluster.confidence
            ),
            "cluster_risk": (
                cluster.risk_score
            ),
        },
        recommendations=[
            "Review funding paths.",
            "Inspect deployer relationships.",
            "Verify Smart Money overlap.",
        ],
    )

    self.cluster_results[
        cluster.id
    ] = result

    self.result_cache[
        cluster.id
    ] = result

    return result


# ==========================================================


def analyze_all_clusters(
    self,
) -> Dict[
    ClusterId,
    ClusterResult,
]:
    """
    Analyze every detected cluster.
    """

    self.statistics[
        "analysis_runs"
    ] += 1

    self.statistics[
        "last_analysis"
    ] = datetime.utcnow()

    results = {}

    for cluster in self.clusters.values():

        result = self.analyze_cluster(
            cluster,
        )

        results[
            cluster.id
        ] = result

    self.update_statistics()

    return results


# ==========================================================


def refresh_cache(
    self,
) -> None:
    """
    Refresh all engine caches.
    """

    self.cluster_cache.clear()

    self.wallet_cache.clear()

    self.similarity_cache.clear()

    self.score_cache.clear()

    self.result_cache.clear()

    for cluster in self.clusters.values():

        self.cluster_cache[
            cluster.id
        ] = cluster

        self.result_cache[
            cluster.id
        ] = self.cluster_results.get(
            cluster.id,
        )

        for node in cluster.wallets:

            self.wallet_cache[
                node.wallet
            ] = cluster.id

            self.score_cache[
                (
                    cluster.cluster_type.value,
                    node.wallet,
                )
            ] = node.score


# ==========================================================


def update_statistics(
    self,
) -> None:
    """
    Recompute engine statistics.
    """

    clusters = list(
        self.clusters.values()
    )

    self.statistics[
        "clusters"
    ] = len(clusters)

    self.statistics[
        "wallets"
    ] = sum(
        cluster.size
        for cluster in clusters
    )

    self.statistics[
        "largest_cluster"
    ] = (
        max(
            (
                cluster.size
                for cluster in clusters
            ),
            default=0,
        )
    )

    self.statistics[
        "average_cluster_size"
    ] = (
        statistics.mean(
            (
                cluster.size
                for cluster in clusters
            )
        )
        if clusters
        else 0.0
    )

    self.statistics[
        "whale_clusters"
    ] = len(
        self.whale_clusters
    )

    self.statistics[
        "smart_money_clusters"
    ] = len(
        self.smart_money_clusters
    )

    self.statistics[
        "wallet_dna_clusters"
    ] = len(
        self.wallet_dna_clusters
    )

    self.statistics[
        "exchange_clusters"
    ] = len(
        self.exchange_clusters
    )

    self.statistics[
        "deployer_clusters"
    ] = len(
        self.deployer_clusters
    )

    self.statistics[
        "graph_nodes"
    ] = self.graph.number_of_nodes()

    self.statistics[
        "graph_edges"
    ] = self.graph.number_of_edges()                