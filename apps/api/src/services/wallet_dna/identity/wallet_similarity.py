# ==========================================================
# Imports
# ==========================================================

from __future__ import annotations

import json
import math
import statistics
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
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

DEFAULT_SIMILARITY_SCORE = 0.0

DEFAULT_CONFIDENCE = 0.50

DEFAULT_MIN_SIMILARITY = 0.70

DEFAULT_MAX_NEIGHBORS = 100

DEFAULT_CACHE_SIZE = 10_000

DEFAULT_ANALYSIS_DEPTH = 20

DEFAULT_LOOKBACK_DAYS = 365

DEFAULT_TIME_WINDOW = timedelta(hours=1)

DEFAULT_MAX_RESULTS = 100

DEFAULT_TIMEOUT_SECONDS = 30

# ==========================================================
# Enums
# ==========================================================

class SimilarityType(Enum):
    """
    Categories of wallet similarity.
    """

    TRANSACTION = "transaction"

    COUNTERPARTY = "counterparty"

    TRADING = "trading"

    FUNDING = "funding"

    TIMING = "timing"

    COMPOSITE = "composite"


class SimilarityLevel(Enum):
    """
    Human-readable similarity level.
    """

    VERY_LOW = "very_low"

    LOW = "low"

    MEDIUM = "medium"

    HIGH = "high"

    VERY_HIGH = "very_high"


# ==========================================================
# Type Aliases
# ==========================================================

WalletAddress: TypeAlias = str

SimilarityScore: TypeAlias = float

Confidence: TypeAlias = float

Timestamp: TypeAlias = datetime

Attributes: TypeAlias = Dict[str, Any]

WalletList: TypeAlias = List[WalletAddress]

WalletSet: TypeAlias = Set[WalletAddress]

SimilarityMatrix: TypeAlias = Dict[
    Tuple[
        WalletAddress,
        WalletAddress,
    ],
    SimilarityScore,
]

SimilarityCache: TypeAlias = Dict[
    Tuple[
        WalletAddress,
        WalletAddress,
    ],
    SimilarityScore,
]

SimilarityStatistics: TypeAlias = Dict[
    str,
    Any,
]

# ==========================================================
# Similarity Result
# ==========================================================

@dataclass(slots=True)
class SimilarityResult:
    """
    Result of comparing two wallets.
    """

    wallet_a: WalletAddress

    wallet_b: WalletAddress

    similarity_type: SimilarityType

    score: SimilarityScore = DEFAULT_SIMILARITY_SCORE

    confidence: Confidence = DEFAULT_CONFIDENCE

    components: Attributes = field(
        default_factory=dict
    )

    explanation: str = ""

    metadata: Attributes = field(
        default_factory=dict
    )

    created_at: Timestamp = field(
        default_factory=datetime.utcnow
    )

    def to_dict(self) -> Dict[str, Any]:

        return {
            "wallet_a": self.wallet_a,
            "wallet_b": self.wallet_b,
            "similarity_type": (
                self.similarity_type.value
            ),
            "score": self.score,
            "confidence": self.confidence,
            "components": self.components,
            "explanation": self.explanation,
            "metadata": self.metadata,
            "created_at": (
                self.created_at.isoformat()
            ),
        }


# ==========================================================
# Similarity Configuration
# ==========================================================

@dataclass(slots=True)
class SimilarityConfig:
    """
    Configuration for WalletSimilarityEngine.
    """

    minimum_similarity: float = (
        DEFAULT_MIN_SIMILARITY
    )

    max_neighbors: int = (
        DEFAULT_MAX_NEIGHBORS
    )

    analysis_depth: int = (
        DEFAULT_ANALYSIS_DEPTH
    )

    cache_size: int = (
        DEFAULT_CACHE_SIZE
    )

    lookback_days: int = (
        DEFAULT_LOOKBACK_DAYS
    )

    time_window: timedelta = (
        DEFAULT_TIME_WINDOW
    )

    timeout_seconds: int = (
        DEFAULT_TIMEOUT_SECONDS
    )

    max_results: int = (
        DEFAULT_MAX_RESULTS
    )

    cache_results: bool = True

    use_cache: bool = True

    enable_transaction_similarity: bool = True

    enable_counterparty_similarity: bool = True

    enable_trading_similarity: bool = True

    enable_funding_similarity: bool = True

    enable_timing_similarity: bool = True

    metadata: Attributes = field(
        default_factory=dict
    )

# ==========================================================
# Wallet Similarity Engine
# ==========================================================

class WalletSimilarityEngine:
    """
    Computes similarity between wallets using:

    • Transaction overlap
    • Shared counterparties
    • Trading behavior
    • Funding sources
    • Timing correlation
    """

    # ======================================================
    # Initialization
    # ======================================================

    def __init__(
        self,
        graph_builder=None,
        relationship_detector=None,
        funding_tracker=None,
        cluster_engine=None,
        config: Optional[
            SimilarityConfig
        ] = None,
    ) -> None:

        self.config = (
            config
            or SimilarityConfig()
        )

        self.graph_builder = graph_builder

        self.relationship_detector = (
            relationship_detector
        )

        self.funding_tracker = (
            funding_tracker
        )

        self.cluster_engine = (
            cluster_engine
        )

        self.graph: nx.Graph = (
            nx.Graph()
        )

        # ==================================================
        # Internal Storage
        # ==================================================

        self.results: Dict[
            Tuple[
                WalletAddress,
                WalletAddress,
            ],
            SimilarityResult,
        ] = {}

        self.wallet_pairs: Set[
            Tuple[
                WalletAddress,
                WalletAddress,
            ]
        ] = set()

        self.similarity_matrix: SimilarityMatrix = {}

        self.neighbor_index: DefaultDict[
            WalletAddress,
            Set[WalletAddress],
        ] = defaultdict(set)

        # ==================================================
        # Cache
        # ==================================================

        self.score_cache: SimilarityCache = {}

        self.transaction_cache: Dict[
            Tuple[
                WalletAddress,
                WalletAddress,
            ],
            float,
        ] = {}

        self.counterparty_cache: Dict[
            Tuple[
                WalletAddress,
                WalletAddress,
            ],
            float,
        ] = {}

        self.trading_cache: Dict[
            Tuple[
                WalletAddress,
                WalletAddress,
            ],
            float,
        ] = {}

        self.funding_cache: Dict[
            Tuple[
                WalletAddress,
                WalletAddress,
            ],
            float,
        ] = {}

        self.timing_cache: Dict[
            Tuple[
                WalletAddress,
                WalletAddress,
            ],
            float,
        ] = {}

        self.result_cache: Dict[
            Tuple[
                WalletAddress,
                WalletAddress,
            ],
            SimilarityResult,
        ] = {}

        # ==================================================
        # Statistics
        # ==================================================

        self.statistics: SimilarityStatistics = {

            "analysis_runs": 0,

            "wallet_pairs": 0,

            "similarity_results": 0,

            "average_similarity": 0.0,

            "highest_similarity": 0.0,

            "cache_hits": 0,

            "cache_misses": 0,

            "transaction_calculations": 0,

            "counterparty_calculations": 0,

            "trading_calculations": 0,

            "funding_calculations": 0,

            "timing_calculations": 0,

            "graph_nodes": 0,

            "graph_edges": 0,

            "last_analysis": None,

        }

# ==========================================================
# Part 3
# Transaction Similarity
# ==========================================================

def shared_transactions(
    self,
    wallet_a: WalletAddress,
    wallet_b: WalletAddress,
) -> List[str]:
    """
    Return transaction signatures shared between
    two wallets.

    A shared transaction is any transaction where
    both wallets participated.
    """

    if self.graph_builder is None:
        return []

    try:

        txs_a = set(
            self.graph_builder
            .wallet_transactions(wallet_a)
        )

        txs_b = set(
            self.graph_builder
            .wallet_transactions(wallet_b)
        )

    except Exception:

        return []

    return sorted(
        txs_a & txs_b
    )


# ==========================================================


def transaction_overlap(
    self,
    wallet_a: WalletAddress,
    wallet_b: WalletAddress,
) -> float:
    """
    Jaccard transaction overlap.

    Returns:
        value in [0,1]
    """

    cache_key = (
        wallet_a,
        wallet_b,
    )

    if cache_key in self.transaction_cache:

        self.statistics["cache_hits"] += 1

        return self.transaction_cache[
            cache_key
        ]

    self.statistics["cache_misses"] += 1

    if self.graph_builder is None:
        return 0.0

    try:

        txs_a = set(
            self.graph_builder
            .wallet_transactions(wallet_a)
        )

        txs_b = set(
            self.graph_builder
            .wallet_transactions(wallet_b)
        )

    except Exception:

        return 0.0

    union = txs_a | txs_b

    if not union:
        return 0.0

    score = len(
        txs_a & txs_b
    ) / len(union)

    self.transaction_cache[
        cache_key
    ] = score

    self.transaction_cache[
        (
            wallet_b,
            wallet_a,
        )
    ] = score

    self.statistics[
        "transaction_calculations"
    ] += 1

    return score


# ==========================================================


def transaction_overlap_score(
    self,
    wallet_a: WalletAddress,
    wallet_b: WalletAddress,
) -> float:
    """
    Enhanced transaction similarity.

    Combines:
        • Jaccard overlap
        • Shared transaction count
        • Relative activity
    """

    overlap = self.transaction_overlap(
        wallet_a,
        wallet_b,
    )

    shared = self.shared_transactions(
        wallet_a,
        wallet_b,
    )

    if self.graph_builder is None:

        return overlap

    try:

        tx_count_a = len(
            self.graph_builder
            .wallet_transactions(wallet_a)
        )

        tx_count_b = len(
            self.graph_builder
            .wallet_transactions(wallet_b)
        )

    except Exception:

        return overlap

    activity_ratio = 0.0

    if tx_count_a and tx_count_b:

        activity_ratio = min(
            tx_count_a,
            tx_count_b,
        ) / max(
            tx_count_a,
            tx_count_b,
        )

    shared_bonus = min(
        len(shared) / 100,
        0.20,
    )

    score = (

        overlap * 0.60 +

        activity_ratio * 0.20 +

        shared_bonus

    )

    return min(
        score,
        1.0,
    )

# ==========================================================
# Part 4
# Counterparty Similarity
# ==========================================================

def shared_counterparties(
    self,
    wallet_a: WalletAddress,
    wallet_b: WalletAddress,
) -> WalletList:
    """
    Return counterparties shared between two wallets.
    """

    if self.graph_builder is None:
        return []

    try:

        cp_a = set(
            self.graph_builder
            .neighbor_wallets(wallet_a)
        )

        cp_b = set(
            self.graph_builder
            .neighbor_wallets(wallet_b)
        )

    except Exception:

        return []

    return sorted(
        cp_a & cp_b
    )


# ==========================================================


def counterparty_overlap(
    self,
    wallet_a: WalletAddress,
    wallet_b: WalletAddress,
) -> float:
    """
    Compute Jaccard overlap of counterparties.

    Returns:
        0.0 → 1.0
    """

    cache_key = (
        wallet_a,
        wallet_b,
    )

    if cache_key in self.counterparty_cache:

        self.statistics["cache_hits"] += 1

        return self.counterparty_cache[
            cache_key
        ]

    self.statistics["cache_misses"] += 1

    if self.graph_builder is None:
        return 0.0

    try:

        cp_a = set(
            self.graph_builder
            .neighbor_wallets(wallet_a)
        )

        cp_b = set(
            self.graph_builder
            .neighbor_wallets(wallet_b)
        )

    except Exception:

        return 0.0

    union = cp_a | cp_b

    if not union:
        return 0.0

    score = len(
        cp_a & cp_b
    ) / len(union)

    self.counterparty_cache[
        cache_key
    ] = score

    self.counterparty_cache[
        (
            wallet_b,
            wallet_a,
        )
    ] = score

    self.statistics[
        "counterparty_calculations"
    ] += 1

    return score


# ==========================================================


def counterparty_score(
    self,
    wallet_a: WalletAddress,
    wallet_b: WalletAddress,
) -> float:
    """
    Enhanced counterparty similarity score.

    Uses:
        • Counterparty overlap
        • Shared counterparties
        • Degree similarity
    """

    overlap = self.counterparty_overlap(
        wallet_a,
        wallet_b,
    )

    shared = self.shared_counterparties(
        wallet_a,
        wallet_b,
    )

    if self.graph_builder is None:

        return overlap

    try:

        degree_a = len(
            self.graph_builder
            .neighbor_wallets(wallet_a)
        )

        degree_b = len(
            self.graph_builder
            .neighbor_wallets(wallet_b)
        )

    except Exception:

        return overlap

    degree_similarity = 0.0

    if degree_a and degree_b:

        degree_similarity = min(
            degree_a,
            degree_b,
        ) / max(
            degree_a,
            degree_b,
        )

    shared_bonus = min(
        len(shared) / 50,
        0.20,
    )

    score = (

        overlap * 0.60 +

        degree_similarity * 0.20 +

        shared_bonus

    )

    return min(
        score,
        1.0,
    )

# ==========================================================
# Part 5
# Trading Behavior Similarity
# ==========================================================

def volume_similarity(
    self,
    wallet_a: WalletAddress,
    wallet_b: WalletAddress,
) -> float:
    """
    Compare total trading volume.

    Returns:
        0.0 → 1.0
    """

    if self.graph_builder is None:
        return 0.0

    try:

        node_a = self.graph_builder.get_node_by_address(
            wallet_a
        )

        node_b = self.graph_builder.get_node_by_address(
            wallet_b
        )

    except Exception:

        return 0.0

    if node_a is None or node_b is None:
        return 0.0

    volume_a = float(node_a.usd_value)

    volume_b = float(node_b.usd_value)

    if volume_a <= 0 and volume_b <= 0:
        return 1.0

    if max(volume_a, volume_b) == 0:
        return 0.0

    return min(
        volume_a,
        volume_b,
    ) / max(
        volume_a,
        volume_b,
    )


# ==========================================================


def token_overlap(
    self,
    wallet_a: WalletAddress,
    wallet_b: WalletAddress,
) -> float:
    """
    Jaccard similarity of traded/held tokens.
    """

    if self.graph_builder is None:
        return 0.0

    try:

        tokens_a = set(
            self.graph_builder.wallet_tokens(
                wallet_a
            )
        )

        tokens_b = set(
            self.graph_builder.wallet_tokens(
                wallet_b
            )
        )

    except Exception:

        return 0.0

    union = tokens_a | tokens_b

    if not union:
        return 0.0

    return len(
        tokens_a & tokens_b
    ) / len(
        union
    )


# ==========================================================


def holding_similarity(
    self,
    wallet_a: WalletAddress,
    wallet_b: WalletAddress,
) -> float:
    """
    Compare wallet holdings.

    Based on SOL balance and token count.
    """

    if self.graph_builder is None:
        return 0.0

    try:

        node_a = self.graph_builder.get_node_by_address(
            wallet_a
        )

        node_b = self.graph_builder.get_node_by_address(
            wallet_b
        )

    except Exception:

        return 0.0

    if node_a is None or node_b is None:
        return 0.0

    balance_similarity = 1.0

    if max(
        node_a.balance_sol,
        node_b.balance_sol,
    ) > 0:

        balance_similarity = (

            min(
                node_a.balance_sol,
                node_b.balance_sol,
            )

            /

            max(
                node_a.balance_sol,
                node_b.balance_sol,
            )

        )

    token_count_similarity = 1.0

    if max(
        node_a.token_count,
        node_b.token_count,
    ) > 0:

        token_count_similarity = (

            min(
                node_a.token_count,
                node_b.token_count,
            )

            /

            max(
                node_a.token_count,
                node_b.token_count,
            )

        )

    return (

        balance_similarity * 0.60

        +

        token_count_similarity * 0.40

    )


# ==========================================================


def trading_pattern_score(
    self,
    wallet_a: WalletAddress,
    wallet_b: WalletAddress,
) -> float:
    """
    Composite trading-pattern similarity.
    """

    volume = self.volume_similarity(
        wallet_a,
        wallet_b,
    )

    tokens = self.token_overlap(
        wallet_a,
        wallet_b,
    )

    holdings = self.holding_similarity(
        wallet_a,
        wallet_b,
    )

    return min(

        volume * 0.30

        +

        tokens * 0.40

        +

        holdings * 0.30,

        1.0,

    )


# ==========================================================


def trading_behavior(
    self,
    wallet_a: WalletAddress,
    wallet_b: WalletAddress,
) -> SimilarityResult:
    """
    Analyze trading behavior similarity.
    """

    score = self.trading_pattern_score(
        wallet_a,
        wallet_b,
    )

    confidence = max(
        0.50,
        score,
    )

    explanation = (
        f"Trading behavior similarity is "
        f"{score:.2f}, based on trading volume, "
        f"token overlap, and holding patterns."
    )

    result = SimilarityResult(

        wallet_a=wallet_a,

        wallet_b=wallet_b,

        similarity_type=SimilarityType.TRADING,

        score=score,

        confidence=confidence,

        components={

            "volume_similarity":
                self.volume_similarity(
                    wallet_a,
                    wallet_b,
                ),

            "token_overlap":
                self.token_overlap(
                    wallet_a,
                    wallet_b,
                ),

            "holding_similarity":
                self.holding_similarity(
                    wallet_a,
                    wallet_b,
                ),

        },

        explanation=explanation,

    )

    self.result_cache[
        (
            wallet_a,
            wallet_b,
        )
    ] = result

    self.statistics[
        "trading_calculations"
    ] += 1

    return result

# ==========================================================
# Part 6
# Funding Similarity
# ==========================================================

def funding_path_similarity(
    self,
    wallet_a: WalletAddress,
    wallet_b: WalletAddress,
) -> float:
    """
    Compare complete funding paths.

    Returns:
        0.0 -> 1.0
    """

    if self.funding_tracker is None:
        return 0.0

    try:

        path_a = (
            self.funding_tracker
            .funding_chain(wallet_a)
        )

        path_b = (
            self.funding_tracker
            .funding_chain(wallet_b)
        )

    except Exception:

        return 0.0

    wallets_a = {
        step.wallet
        for step in path_a
    }

    wallets_b = {
        step.wallet
        for step in path_b
    }

    union = wallets_a | wallets_b

    if not union:
        return 0.0

    return len(
        wallets_a & wallets_b
    ) / len(union)


# ==========================================================


def common_funder_score(
    self,
    wallet_a: WalletAddress,
    wallet_b: WalletAddress,
) -> float:
    """
    Score based on common funding wallets.
    """

    if self.funding_tracker is None:
        return 0.0

    try:

        common = (
            self.funding_tracker
            .common_funders(
                wallet_a,
                wallet_b,
            )
        )

    except Exception:

        return 0.0

    if not common:
        return 0.0

    score = 0.0

    for wallet in common:

        confidence = 1.0

        try:

            confidence = (
                self.funding_tracker
                .funding_confidence(
                    wallet
                )
            )

        except Exception:

            pass

        score += confidence

    score /= len(common)

    return min(
        score,
        1.0,
    )


# ==========================================================


def funding_chain_similarity(
    self,
    wallet_a: WalletAddress,
    wallet_b: WalletAddress,
) -> float:
    """
    Composite funding-chain similarity.
    """

    path_similarity = (
        self.funding_path_similarity(
            wallet_a,
            wallet_b,
        )
    )

    common_score = (
        self.common_funder_score(
            wallet_a,
            wallet_b,
        )
    )

    return min(

        path_similarity * 0.60

        +

        common_score * 0.40,

        1.0,

    )


# ==========================================================


def funding_similarity(
    self,
    wallet_a: WalletAddress,
    wallet_b: WalletAddress,
) -> SimilarityResult:
    """
    Analyze funding similarity between
    two wallets.
    """

    score = (
        self.funding_chain_similarity(
            wallet_a,
            wallet_b,
        )
    )

    confidence = max(
        0.50,
        score,
    )

    explanation = (
        f"Funding similarity score "
        f"{score:.2f}, based on "
        f"shared funding paths and "
        f"common funders."
    )

    result = SimilarityResult(

        wallet_a=wallet_a,

        wallet_b=wallet_b,

        similarity_type=SimilarityType.FUNDING,

        score=score,

        confidence=confidence,

        components={

            "funding_path_similarity":
                self.funding_path_similarity(
                    wallet_a,
                    wallet_b,
                ),

            "common_funder_score":
                self.common_funder_score(
                    wallet_a,
                    wallet_b,
                ),

        },

        explanation=explanation,

    )

    self.funding_cache[
        (
            wallet_a,
            wallet_b,
        )
    ] = score

    self.result_cache[
        (
            wallet_a,
            wallet_b,
        )
    ] = result

    self.statistics[
        "funding_calculations"
    ] += 1

    return result

# ==========================================================
# Part 7
# Timing Correlation
# ==========================================================

def transaction_time_overlap(
    self,
    wallet_a: WalletAddress,
    wallet_b: WalletAddress,
) -> float:
    """
    Compute the overlap between transaction timestamps
    for two wallets using the configured time window.

    Returns:
        0.0 -> 1.0
    """

    if self.graph_builder is None:
        return 0.0

    try:

        txs_a = self.graph_builder.wallet_transactions(
            wallet_a
        )

        txs_b = self.graph_builder.wallet_transactions(
            wallet_b
        )

    except Exception:

        return 0.0

    if not txs_a or not txs_b:
        return 0.0

    timestamps_a = sorted(
        tx.block_time
        for tx in txs_a
        if getattr(tx, "block_time", None)
    )

    timestamps_b = sorted(
        tx.block_time
        for tx in txs_b
        if getattr(tx, "block_time", None)
    )

    if not timestamps_a or not timestamps_b:
        return 0.0

    overlap = 0

    for ts_a in timestamps_a:

        for ts_b in timestamps_b:

            if abs(
                ts_a - ts_b
            ) <= self.config.time_window:

                overlap += 1
                break

    denominator = max(
        len(timestamps_a),
        len(timestamps_b),
    )

    return overlap / denominator


# ==========================================================


def activity_window_similarity(
    self,
    wallet_a: WalletAddress,
    wallet_b: WalletAddress,
) -> float:
    """
    Compare activity distribution throughout the day.

    Wallets that trade during similar hours
    receive higher scores.
    """

    if self.graph_builder is None:
        return 0.0

    try:

        txs_a = self.graph_builder.wallet_transactions(
            wallet_a
        )

        txs_b = self.graph_builder.wallet_transactions(
            wallet_b
        )

    except Exception:

        return 0.0

    hours_a = Counter(
        tx.block_time.hour
        for tx in txs_a
        if getattr(tx, "block_time", None)
    )

    hours_b = Counter(
        tx.block_time.hour
        for tx in txs_b
        if getattr(tx, "block_time", None)
    )

    if not hours_a or not hours_b:
        return 0.0

    similarity = 0.0

    total = sum(hours_a.values()) + sum(hours_b.values())

    for hour in range(24):

        similarity += min(
            hours_a.get(hour, 0),
            hours_b.get(hour, 0),
        )

    return (
        (2 * similarity) / total
        if total
        else 0.0
    )


# ==========================================================


def temporal_score(
    self,
    wallet_a: WalletAddress,
    wallet_b: WalletAddress,
) -> float:
    """
    Composite temporal similarity.
    """

    overlap = self.transaction_time_overlap(
        wallet_a,
        wallet_b,
    )

    activity = self.activity_window_similarity(
        wallet_a,
        wallet_b,
    )

    return min(

        overlap * 0.60 +

        activity * 0.40,

        1.0,

    )


# ==========================================================


def timing_correlation(
    self,
    wallet_a: WalletAddress,
    wallet_b: WalletAddress,
) -> SimilarityResult:
    """
    Analyze timing correlation between wallets.
    """

    score = self.temporal_score(
        wallet_a,
        wallet_b,
    )

    confidence = max(
        DEFAULT_CONFIDENCE,
        score,
    )

    result = SimilarityResult(

        wallet_a=wallet_a,

        wallet_b=wallet_b,

        similarity_type=SimilarityType.TIMING,

        score=score,

        confidence=confidence,

        components={

            "transaction_overlap":
                self.transaction_time_overlap(
                    wallet_a,
                    wallet_b,
                ),

            "activity_window":
                self.activity_window_similarity(
                    wallet_a,
                    wallet_b,
                ),

        },

        explanation=(
            f"Temporal similarity "
            f"{score:.2f}, based on "
            "transaction timing and "
            "daily activity windows."
        ),

    )

    self.timing_cache[
        (
            wallet_a,
            wallet_b,
        )
    ] = score

    self.result_cache[
        (
            wallet_a,
            wallet_b,
        )
    ] = result

    self.statistics[
        "timing_calculations"
    ] += 1

    return result

# ==========================================================
# Part 8
# Composite Similarity
# ==========================================================

def similarity_components(
    self,
    wallet_a: WalletAddress,
    wallet_b: WalletAddress,
) -> Dict[str, float]:
    """
    Compute every similarity component between
    two wallets.
    """

    return {

        "transaction": self.transaction_overlap_score(
            wallet_a,
            wallet_b,
        ),

        "counterparty": self.counterparty_score(
            wallet_a,
            wallet_b,
        ),

        "trading": self.trading_pattern_score(
            wallet_a,
            wallet_b,
        ),

        "funding": self.funding_chain_similarity(
            wallet_a,
            wallet_b,
        ),

        "timing": self.temporal_score(
            wallet_a,
            wallet_b,
        ),

    }


# ==========================================================


def overall_similarity(
    self,
    wallet_a: WalletAddress,
    wallet_b: WalletAddress,
) -> float:
    """
    Overall Wallet DNA similarity score.

    Weighted composite.
    """

    cache_key = (
        wallet_a,
        wallet_b,
    )

    if cache_key in self.score_cache:

        self.statistics["cache_hits"] += 1

        return self.score_cache[
            cache_key
        ]

    self.statistics["cache_misses"] += 1

    c = self.similarity_components(
        wallet_a,
        wallet_b,
    )

    score = (

        c["transaction"] * 0.25 +

        c["counterparty"] * 0.20 +

        c["trading"] * 0.20 +

        c["funding"] * 0.20 +

        c["timing"] * 0.15

    )

    score = min(
        score,
        1.0,
    )

    self.score_cache[
        cache_key
    ] = score

    self.score_cache[
        (
            wallet_b,
            wallet_a,
        )
    ] = score

    return score


# ==========================================================


def confidence(
    self,
    wallet_a: WalletAddress,
    wallet_b: WalletAddress,
) -> float:
    """
    Confidence of the composite similarity.

    Higher agreement between components produces
    higher confidence.
    """

    components = list(

        self.similarity_components(
            wallet_a,
            wallet_b,
        ).values()

    )

    if not components:
        return DEFAULT_CONFIDENCE

    mean = statistics.mean(
        components
    )

    deviation = statistics.pstdev(
        components
    )

    confidence = (

        mean *

        (1.0 - deviation)

    )

    return max(
        DEFAULT_CONFIDENCE,
        min(
            confidence,
            1.0,
        ),
    )


# ==========================================================


def explain_similarity(
    self,
    wallet_a: WalletAddress,
    wallet_b: WalletAddress,
) -> str:
    """
    Generate an AI-readable explanation.
    """

    c = self.similarity_components(
        wallet_a,
        wallet_b,
    )

    strongest = max(
        c.items(),
        key=lambda x: x[1],
    )

    weakest = min(
        c.items(),
        key=lambda x: x[1],
    )

    return (

        f"Wallet similarity is driven primarily by "

        f"{strongest[0]} similarity "

        f"({strongest[1]:.2f}). "

        f"The weakest signal is "

        f"{weakest[0]} "

        f"({weakest[1]:.2f}). "

        f"Overall similarity "

        f"{self.overall_similarity(wallet_a, wallet_b):.2f}."

    )


# ==========================================================


def similarity_summary(
    self,
    wallet_a: WalletAddress,
    wallet_b: WalletAddress,
) -> Dict[str, Any]:
    """
    Produce a complete similarity summary.
    """

    components = self.similarity_components(
        wallet_a,
        wallet_b,
    )

    return {

        "wallet_a": wallet_a,

        "wallet_b": wallet_b,

        "overall_similarity":
            self.overall_similarity(
                wallet_a,
                wallet_b,
            ),

        "confidence":
            self.confidence(
                wallet_a,
                wallet_b,
            ),

        "components":
            components,

        "level": (

            SimilarityLevel.VERY_HIGH.value
            if self.overall_similarity(
                wallet_a,
                wallet_b,
            ) >= 0.90

            else SimilarityLevel.HIGH.value
            if self.overall_similarity(
                wallet_a,
                wallet_b,
            ) >= 0.75

            else SimilarityLevel.MEDIUM.value
            if self.overall_similarity(
                wallet_a,
                wallet_b,
            ) >= 0.50

            else SimilarityLevel.LOW.value
            if self.overall_similarity(
                wallet_a,
                wallet_b,
            ) >= 0.25

            else SimilarityLevel.VERY_LOW.value

        ),

        "explanation":
            self.explain_similarity(
                wallet_a,
                wallet_b,
            ),

    }

# ==========================================================
# Part 9
# Analytics
# ==========================================================

def nearest_neighbors(
    self,
    wallet: WalletAddress,
    *,
    limit: int = 10,
    minimum_score: float = 0.0,
) -> List[Tuple[WalletAddress, float]]:
    """
    Return the nearest neighboring wallets ordered by
    overall similarity.
    """

    if self.graph_builder is None:
        return []

    neighbors: List[
        Tuple[
            WalletAddress,
            float,
        ]
    ] = []

    try:

        wallets = list(
            self.graph_builder.address_index.keys()
        )

    except Exception:

        return []

    for other in wallets:

        if other == wallet:
            continue

        score = self.overall_similarity(
            wallet,
            other,
        )

        if score >= minimum_score:

            neighbors.append(
                (
                    other,
                    score,
                )
            )

    neighbors.sort(
        key=lambda item: item[1],
        reverse=True,
    )

    return neighbors[:limit]


# ==========================================================


def most_similar_wallets(
    self,
    *,
    limit: int = 25,
    minimum_score: float = 0.75,
) -> List[
    Tuple[
        WalletAddress,
        WalletAddress,
        float,
    ]
]:
    """
    Return the highest-scoring wallet pairs.
    """

    if self.graph_builder is None:
        return []

    try:

        wallets = list(
            self.graph_builder.address_index.keys()
        )

    except Exception:

        return []

    results = []

    for i, wallet_a in enumerate(wallets):

        for wallet_b in wallets[i + 1:]:

            score = self.overall_similarity(
                wallet_a,
                wallet_b,
            )

            if score >= minimum_score:

                results.append(
                    (
                        wallet_a,
                        wallet_b,
                        score,
                    )
                )

    results.sort(
        key=lambda item: item[2],
        reverse=True,
    )

    return results[:limit]


# ==========================================================


def similarity_matrix(
    self,
) -> SimilarityMatrix:
    """
    Build a complete similarity matrix.

    Also stores it internally.
    """

    matrix: SimilarityMatrix = {}

    if self.graph_builder is None:

        return matrix

    try:

        wallets = list(
            self.graph_builder.address_index.keys()
        )

    except Exception:

        return matrix

    for i, wallet_a in enumerate(wallets):

        for wallet_b in wallets[i:]:

            score = (

                1.0

                if wallet_a == wallet_b

                else self.overall_similarity(
                    wallet_a,
                    wallet_b,
                )

            )

            matrix[
                (
                    wallet_a,
                    wallet_b,
                )
            ] = score

            matrix[
                (
                    wallet_b,
                    wallet_a,
                )
            ] = score

    self.similarity_matrix = matrix

    return matrix


# ==========================================================


def statistics(
    self,
) -> Dict[str, Any]:
    """
    Return analytics for the similarity engine.
    """

    scores = list(
        self.score_cache.values()
    )

    return {

        "wallet_pairs": len(
            self.score_cache,
        ),

        "similarity_results": len(
            self.result_cache,
        ),

        "average_similarity": (

            statistics.mean(scores)

            if scores

            else 0.0

        ),

        "median_similarity": (

            statistics.median(scores)

            if scores

            else 0.0

        ),

        "highest_similarity": (

            max(scores)

            if scores

            else 0.0

        ),

        "lowest_similarity": (

            min(scores)

            if scores

            else 0.0

        ),

        "cache_hits":
            self.statistics.get(
                "cache_hits",
                0,
            ),

        "cache_misses":
            self.statistics.get(
                "cache_misses",
                0,
            ),

        "analysis_runs":
            self.statistics.get(
                "analysis_runs",
                0,
            ),

        "transaction_calculations":
            self.statistics.get(
                "transaction_calculations",
                0,
            ),

        "counterparty_calculations":
            self.statistics.get(
                "counterparty_calculations",
                0,
            ),

        "trading_calculations":
            self.statistics.get(
                "trading_calculations",
                0,
            ),

        "funding_calculations":
            self.statistics.get(
                "funding_calculations",
                0,
            ),

        "timing_calculations":
            self.statistics.get(
                "timing_calculations",
                0,
            ),

        "graph_nodes":
            self.statistics.get(
                "graph_nodes",
                0,
            ),

        "graph_edges":
            self.statistics.get(
                "graph_edges",
                0,
            ),

        "last_analysis":
            self.statistics.get(
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
    Export the complete WalletSimilarityEngine state.
    """

    return {

        "results": {

            f"{a}->{b}": result.to_dict()

            for (a, b), result in self.result_cache.items()

        },

        "statistics": self.statistics(),

        "config": vars(self.config),

        "metadata": {

            "wallet_pairs": len(self.score_cache),

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
    Export WalletSimilarityEngine as JSON.
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
    Export similarity results as a pandas DataFrame.
    """

    try:

        import pandas as pd

    except ImportError as exc:

        raise ImportError(
            "pandas is required for to_dataframe()."
        ) from exc

    rows = []

    for result in self.result_cache.values():

        rows.append({

            "wallet_a": result.wallet_a,

            "wallet_b": result.wallet_b,

            "type": result.similarity_type.value,

            "score": result.score,

            "confidence": result.confidence,

            **result.components,

            "explanation": result.explanation,

            "created_at": result.created_at,

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
    Save similarity results as JSON.
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
        Union[
            str,
            Path,
        ]
    ] = None,
):
    """
    Export similarity results to CSV.

    Returns DataFrame if path is None.
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

def analyze_pair(
    self,
    wallet_a: WalletAddress,
    wallet_b: WalletAddress,
) -> SimilarityResult:
    """
    Analyze a single wallet pair.

    Computes every similarity component and stores
    the result in the internal caches.
    """

    result = SimilarityResult(

        wallet_a=wallet_a,

        wallet_b=wallet_b,

        similarity_type=SimilarityType.COMPOSITE,

        score=self.overall_similarity(
            wallet_a,
            wallet_b,
        ),

        confidence=self.confidence(
            wallet_a,
            wallet_b,
        ),

        components=self.similarity_components(
            wallet_a,
            wallet_b,
        ),

        explanation=self.explain_similarity(
            wallet_a,
            wallet_b,
        ),

    )

    key = tuple(
        sorted(
            (
                wallet_a,
                wallet_b,
            )
        )
    )

    self.result_cache[key] = result

    self.results[key] = result

    self.score_cache[key] = result.score

    return result


# ==========================================================


def analyze_all(
    self,
) -> Dict[
    Tuple[
        WalletAddress,
        WalletAddress,
    ],
    SimilarityResult,
]:
    """
    Analyze every wallet pair in the graph.
    """

    if self.graph_builder is None:
        return {}

    self.statistics[
        "analysis_runs"
    ] += 1

    self.statistics[
        "last_analysis"
    ] = datetime.utcnow()

    try:

        wallets = list(
            self.graph_builder.address_index.keys()
        )

    except Exception:

        return {}

    for i, wallet_a in enumerate(wallets):

        for wallet_b in wallets[i + 1:]:

            self.analyze_pair(
                wallet_a,
                wallet_b,
            )

    self.update_statistics()

    return self.result_cache


# ==========================================================


def refresh_cache(
    self,
) -> None:
    """
    Rebuild every internal cache.
    """

    self.score_cache.clear()

    self.transaction_cache.clear()

    self.counterparty_cache.clear()

    self.trading_cache.clear()

    self.funding_cache.clear()

    self.timing_cache.clear()

    self.result_cache.clear()

    self.similarity_matrix.clear()

    self.wallet_pairs.clear()

    self.neighbor_index.clear()

    if self.graph_builder is None:
        return

    try:

        wallets = list(
            self.graph_builder.address_index.keys()
        )

    except Exception:

        return

    for i, wallet_a in enumerate(wallets):

        for wallet_b in wallets[i + 1:]:

            result = self.analyze_pair(
                wallet_a,
                wallet_b,
            )

            key = tuple(
                sorted(
                    (
                        wallet_a,
                        wallet_b,
                    )
                )
            )

            self.wallet_pairs.add(
                key
            )

            self.similarity_matrix[
                key
            ] = result.score

            self.neighbor_index[
                wallet_a
            ].add(
                wallet_b
            )

            self.neighbor_index[
                wallet_b
            ].add(
                wallet_a
            )


# ==========================================================


def update_statistics(
    self,
) -> None:
    """
    Update engine-wide statistics.
    """

    scores = list(
        self.score_cache.values()
    )

    self.statistics[
        "wallet_pairs"
    ] = len(
        self.wallet_pairs
    )

    self.statistics[
        "similarity_results"
    ] = len(
        self.result_cache
    )

    self.statistics[
        "average_similarity"
    ] = (

        statistics.mean(
            scores
        )

        if scores

        else 0.0

    )

    self.statistics[
        "highest_similarity"
    ] = (

        max(scores)

        if scores

        else 0.0

    )

    self.statistics[
        "graph_nodes"
    ] = (

        self.graph.number_of_nodes()

        if self.graph

        else 0

    )

    self.statistics[
        "graph_edges"
    ] = (

        self.graph.number_of_edges()

        if self.graph

        else 0

    )                


