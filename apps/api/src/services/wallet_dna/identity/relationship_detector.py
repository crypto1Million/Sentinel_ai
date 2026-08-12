"""
Sentinel AI
Wallet DNA Relationship Detector

Detects relationships between wallets using:

• Shared Funding
• Shared Deployers
• Common Counterparties
• Circular Transfers
• Hidden Relationships
• Multi-Wallet Ownership
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import (
    Any,
    Dict,
    FrozenSet,
    Iterable,
    List,
    Optional,
    Set,
    Tuple,
    TypeAlias,
)

from collections import defaultdict, deque

import networkx as nx

from .graph_builder import (
    GraphBuilder,
    WalletNode,
    GraphEdge,
    NodeId,
    EdgeId,
)

# ==========================================================
# Constants
# ==========================================================

DEFAULT_RELATIONSHIP_THRESHOLD = 0.50

DEFAULT_SHARED_FUNDER_THRESHOLD = 2

DEFAULT_COUNTERPARTY_THRESHOLD = 3

DEFAULT_CYCLE_DEPTH = 6

DEFAULT_MAX_SEARCH_DEPTH = 5

DEFAULT_CONFIDENCE = 1.0

MAX_CLUSTER_SIZE = 500

MAX_PATHS = 1000

MAX_COMMON_COUNTERPARTIES = 100

# ==========================================================
# Type Aliases
# ==========================================================

WalletPair: TypeAlias = Tuple[NodeId, NodeId]

WalletSet: TypeAlias = Set[NodeId]

WalletCluster: TypeAlias = Set[NodeId]

WalletClusters: TypeAlias = List[WalletCluster]

RelationshipScore: TypeAlias = float

ConfidenceScore: TypeAlias = float

RiskScore: TypeAlias = float

SimilarityScore: TypeAlias = float

CounterpartyMap: TypeAlias = Dict[
    NodeId,
    Set[NodeId],
]

FundingMap: TypeAlias = Dict[
    NodeId,
    Set[NodeId],
]

RelationshipMatrix: TypeAlias = Dict[
    WalletPair,
    RelationshipScore,
]

RelationshipCache: TypeAlias = Dict[
    WalletPair,
    Any,
]

Metadata: TypeAlias = Dict[
    str,
    Any,
]

# ==========================================================
# Relationship Types
# ==========================================================

class RelationshipType(str, Enum):
    """
    Supported wallet relationship categories.
    """

    SHARED_FUNDER = "shared_funder"

    SHARED_DEPLOYER = "shared_deployer"

    COMMON_COUNTERPARTY = "common_counterparty"

    CIRCULAR_TRANSFER = "circular_transfer"

    HIDDEN_RELATIONSHIP = "hidden_relationship"

    MULTI_WALLET_OWNER = "multi_wallet_owner"

    SHARED_LIQUIDITY = "shared_liquidity"

    SHARED_TOKEN = "shared_token"

    SHARED_JITO = "shared_jito"

    SHARED_MEV = "shared_mev"

    CAPITAL_FLOW = "capital_flow"

    FUNDING_CHAIN = "funding_chain"

    INDIRECT_CONNECTION = "indirect_connection"

    BEHAVIORAL_SIMILARITY = "behavioral_similarity"

    UNKNOWN = "unknown"


# ==========================================================
# Relationship Result
# ==========================================================

@dataclass(slots=True)
class RelationshipResult:
    """
    Result of a relationship detection.
    """

    wallet_a: NodeId

    wallet_b: NodeId

    relationship_type: RelationshipType

    score: RelationshipScore = 0.0

    confidence: ConfidenceScore = DEFAULT_CONFIDENCE

    risk_score: RiskScore = 0.0

    evidence: List[str] = field(
        default_factory=list
    )

    common_wallets: WalletSet = field(
        default_factory=set
    )

    common_transactions: int = 0

    common_tokens: int = 0

    path_length: Optional[int] = None

    metadata: Metadata = field(
        default_factory=dict
    )

    detected_at: datetime = field(
        default_factory=datetime.utcnow
    )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "wallet_a": self.wallet_a,
            "wallet_b": self.wallet_b,
            "relationship_type": self.relationship_type.value,
            "score": self.score,
            "confidence": self.confidence,
            "risk_score": self.risk_score,
            "evidence": list(self.evidence),
            "common_wallets": list(
                self.common_wallets
            ),
            "common_transactions": self.common_transactions,
            "common_tokens": self.common_tokens,
            "path_length": self.path_length,
            "metadata": self.metadata,
            "detected_at": self.detected_at.isoformat(),
        }


# ==========================================================
# Detection Configuration
# ==========================================================

@dataclass(slots=True)
class DetectionConfig:
    """
    Relationship detection configuration.
    """

    relationship_threshold: float = (
        DEFAULT_RELATIONSHIP_THRESHOLD
    )

    shared_funder_threshold: int = (
        DEFAULT_SHARED_FUNDER_THRESHOLD
    )

    counterparty_threshold: int = (
        DEFAULT_COUNTERPARTY_THRESHOLD
    )

    max_search_depth: int = (
        DEFAULT_MAX_SEARCH_DEPTH
    )

    cycle_depth: int = (
        DEFAULT_CYCLE_DEPTH
    )

    max_paths: int = MAX_PATHS

    max_cluster_size: int = (
        MAX_CLUSTER_SIZE
    )

    enable_shared_funding: bool = True

    enable_shared_deployer: bool = True

    enable_counterparty: bool = True

    enable_circular_transfer: bool = True

    enable_hidden_relationships: bool = True

    enable_multi_wallet_detection: bool = True

    enable_behavioral_similarity: bool = True

    use_cache: bool = True

    cache_results: bool = True

    include_low_confidence: bool = False

    min_confidence: float = 0.50

    metadata: Metadata = field(
        default_factory=dict
    )

# ==========================================================
# Relationship Detector
# ==========================================================

class RelationshipDetector:
    """
    Wallet DNA relationship detection engine.

    Detects:

    • Shared funding
    • Shared deployers
    • Common counterparties
    • Circular transfers
    • Hidden relationships
    • Multi-wallet ownership
    """

    def __init__(
        self,
        graph: GraphBuilder,
        config: Optional[
            DetectionConfig
        ] = None,
    ) -> None:

        self.graph = graph

        self.config = (
            config
            if config is not None
            else DetectionConfig()
        )

        # --------------------------------------------------
        # Detection Results
        # --------------------------------------------------

        self.relationships: List[
            RelationshipResult
        ] = []

        self.relationship_matrix: RelationshipMatrix = {}

        # --------------------------------------------------
        # Wallet Indexes
        # --------------------------------------------------

        self.wallet_index: Dict[
            NodeId,
            WalletNode,
        ] = dict(
            self.graph.nodes
        )

        self.edge_index: Dict[
            EdgeId,
            GraphEdge,
        ] = dict(
            self.graph.edges
        )

        # --------------------------------------------------
        # Funding Cache
        # --------------------------------------------------

        self.funding_map: FundingMap = (
            defaultdict(set)
        )

        self.reverse_funding_map: FundingMap = (
            defaultdict(set)
        )

        # --------------------------------------------------
        # Counterparty Cache
        # --------------------------------------------------

        self.counterparty_map: CounterpartyMap = (
            defaultdict(set)
        )

        # --------------------------------------------------
        # Cluster Storage
        # --------------------------------------------------

        self.wallet_clusters: WalletClusters = []

        # --------------------------------------------------
        # Similarity Cache
        # --------------------------------------------------

        self.similarity_cache: Dict[
            WalletPair,
            SimilarityScore,
        ] = {}

        # --------------------------------------------------
        # Relationship Cache
        # --------------------------------------------------

        self.relationship_cache: RelationshipCache = {}

        # --------------------------------------------------
        # Hidden Relationship Cache
        # --------------------------------------------------

        self.hidden_relationship_cache: Dict[
            WalletPair,
            List[NodeId],
        ] = {}

        # --------------------------------------------------
        # Circular Transfer Cache
        # --------------------------------------------------

        self.circular_transfer_cache: Dict[
            WalletPair,
            List[List[NodeId]],
        ] = {}

        # --------------------------------------------------
        # Statistics
        # --------------------------------------------------

        self.statistics: Dict[
            str,
            Any,
        ] = {
            "wallets": len(
                self.graph.nodes
            ),
            "edges": len(
                self.graph.edges
            ),
            "relationships": 0,
            "clusters": 0,
            "detections": 0,
            "last_run": None,
        }

        # --------------------------------------------------
        # Internal Flags
        # --------------------------------------------------

        self._initialized = False

        self._graph_loaded = False

        self._indexes_ready = False

        self._cache_ready = False

        # --------------------------------------------------
        # Initialize
        # --------------------------------------------------

        self._initialize()

# ==========================================================
# Part 2
# Funding Detection
# ==========================================================

def common_funders(
    self,
    wallet_a: NodeId,
    wallet_b: NodeId,
) -> WalletSet:
    """
    Return wallets that funded both wallets.
    """

    if wallet_a not in self.wallet_index:
        raise KeyError(
            f"Unknown wallet '{wallet_a}'."
        )

    if wallet_b not in self.wallet_index:
        raise KeyError(
            f"Unknown wallet '{wallet_b}'."
        )

    funders_a = self.reverse_funding_map.get(
        wallet_a,
        set(),
    )

    funders_b = self.reverse_funding_map.get(
        wallet_b,
        set(),
    )

    return set(funders_a).intersection(
        funders_b
    )


def shared_funding_score(
    self,
    wallet_a: NodeId,
    wallet_b: NodeId,
) -> float:
    """
    Calculate funding similarity score.

    Uses Jaccard similarity.
    """

    funders_a = self.reverse_funding_map.get(
        wallet_a,
        set(),
    )

    funders_b = self.reverse_funding_map.get(
        wallet_b,
        set(),
    )

    if not funders_a and not funders_b:
        return 0.0

    intersection = funders_a.intersection(
        funders_b
    )

    union = funders_a.union(
        funders_b
    )

    if not union:
        return 0.0

    return len(intersection) / len(union)


def detect_shared_funding(
    self,
    wallet_a: NodeId,
    wallet_b: NodeId,
) -> Optional[RelationshipResult]:
    """
    Detect shared funding between two wallets.
    """

    common = self.common_funders(
        wallet_a,
        wallet_b,
    )

    if (
        len(common)
        < self.config.shared_funder_threshold
    ):
        return None

    score = self.shared_funding_score(
        wallet_a,
        wallet_b,
    )

    confidence = min(
        1.0,
        score + (
            len(common) * 0.10
        ),
    )

    result = RelationshipResult(
        wallet_a=wallet_a,
        wallet_b=wallet_b,
        relationship_type=RelationshipType.SHARED_FUNDER,
        score=score,
        confidence=confidence,
        risk_score=score,
        common_wallets=common,
        evidence=[
            (
                f"{len(common)} "
                "shared funding wallet(s)"
            )
        ],
        metadata={
            "shared_funders": list(
                common
            ),
            "shared_funder_count": len(
                common
            ),
        },
    )

    self.relationships.append(
        result
    )

    self.relationship_matrix[
        (
            wallet_a,
            wallet_b,
        )
    ] = score

    self.relationship_cache[
        (
            wallet_a,
            wallet_b,
        )
    ] = result

    self.statistics[
        "relationships"
    ] += 1

    self.statistics[
        "detections"
    ] += 1

    self.statistics[
        "last_run"
    ] = datetime.utcnow()

    return result

# ==========================================================
# Part 3
# Deployer Detection
# ==========================================================

def related_deployer_wallets(
    self,
    deployer_wallet: NodeId,
) -> WalletSet:
    """
    Return every wallet deployed by the same deployer.
    """

    if deployer_wallet not in self.wallet_index:
        raise KeyError(
            f"Unknown wallet '{deployer_wallet}'."
        )

    related: WalletSet = set()

    deployer = self.wallet_index[
        deployer_wallet
    ]

    deployer_address = deployer.metadata.get(
        "deployer"
    )

    if deployer_address is None:
        return related

    for node in self.wallet_index.values():

        if (
            node.metadata.get("deployer")
            == deployer_address
        ):
            related.add(node.id)

    return related


def deployer_similarity(
    self,
    wallet_a: NodeId,
    wallet_b: NodeId,
) -> float:
    """
    Compute similarity based on deployer.

    Returns:
        1.0 -> same deployer
        0.0 -> different deployers
    """

    if wallet_a not in self.wallet_index:
        raise KeyError(
            f"Unknown wallet '{wallet_a}'."
        )

    if wallet_b not in self.wallet_index:
        raise KeyError(
            f"Unknown wallet '{wallet_b}'."
        )

    deployer_a = self.wallet_index[
        wallet_a
    ].metadata.get("deployer")

    deployer_b = self.wallet_index[
        wallet_b
    ].metadata.get("deployer")

    if deployer_a is None:
        return 0.0

    if deployer_b is None:
        return 0.0

    return float(
        deployer_a == deployer_b
    )


def detect_shared_deployer(
    self,
    wallet_a: NodeId,
    wallet_b: NodeId,
) -> Optional[RelationshipResult]:
    """
    Detect whether two wallets originate
    from the same deployer.
    """

    score = self.deployer_similarity(
        wallet_a,
        wallet_b,
    )

    if score <= 0.0:
        return None

    deployer = self.wallet_index[
        wallet_a
    ].metadata.get("deployer")

    related = self.related_deployer_wallets(
        wallet_a
    )

    confidence = min(
        1.0,
        0.75 + (
            len(related) * 0.02
        ),
    )

    result = RelationshipResult(
        wallet_a=wallet_a,
        wallet_b=wallet_b,
        relationship_type=RelationshipType.SHARED_DEPLOYER,
        score=score,
        confidence=confidence,
        risk_score=score,
        common_wallets=related,
        evidence=[
            (
                "Same deployer detected: "
                f"{deployer}"
            )
        ],
        metadata={
            "deployer": deployer,
            "related_wallets": list(
                related
            ),
            "wallet_count": len(
                related
            ),
        },
    )

    self.relationships.append(
        result
    )

    self.relationship_matrix[
        (
            wallet_a,
            wallet_b,
        )
    ] = score

    self.relationship_cache[
        (
            wallet_a,
            wallet_b,
        )
    ] = result

    self.statistics[
        "relationships"
    ] += 1

    self.statistics[
        "detections"
    ] += 1

    self.statistics[
        "last_run"
    ] = datetime.utcnow()

    return result

# ==========================================================
# Part 4
# Counterparty Analysis
# ==========================================================

def common_counterparties(
    self,
    wallet_a: NodeId,
    wallet_b: NodeId,
) -> WalletSet:
    """
    Return counterparties shared by two wallets.
    """

    if wallet_a not in self.wallet_index:
        raise KeyError(
            f"Unknown wallet '{wallet_a}'."
        )

    if wallet_b not in self.wallet_index:
        raise KeyError(
            f"Unknown wallet '{wallet_b}'."
        )

    counterparties_a = self.counterparty_map.get(
        wallet_a,
        set(),
    )

    counterparties_b = self.counterparty_map.get(
        wallet_b,
        set(),
    )

    return counterparties_a.intersection(
        counterparties_b
    )


def counterparty_similarity(
    self,
    wallet_a: NodeId,
    wallet_b: NodeId,
) -> float:
    """
    Jaccard similarity of counterparties.
    """

    counterparties_a = self.counterparty_map.get(
        wallet_a,
        set(),
    )

    counterparties_b = self.counterparty_map.get(
        wallet_b,
        set(),
    )

    if (
        not counterparties_a
        and not counterparties_b
    ):
        return 0.0

    union = counterparties_a.union(
        counterparties_b
    )

    if not union:
        return 0.0

    intersection = counterparties_a.intersection(
        counterparties_b
    )

    return (
        len(intersection)
        / len(union)
    )


def shared_interactions(
    self,
    wallet_a: NodeId,
    wallet_b: NodeId,
) -> Optional[RelationshipResult]:
    """
    Detect relationship through common counterparties.
    """

    common = self.common_counterparties(
        wallet_a,
        wallet_b,
    )

    if (
        len(common)
        < self.config.counterparty_threshold
    ):
        return None

    similarity = self.counterparty_similarity(
        wallet_a,
        wallet_b,
    )

    confidence = min(
        1.0,
        similarity
        + (len(common) * 0.05),
    )

    result = RelationshipResult(
        wallet_a=wallet_a,
        wallet_b=wallet_b,
        relationship_type=RelationshipType.COMMON_COUNTERPARTY,
        score=similarity,
        confidence=confidence,
        risk_score=similarity,
        common_wallets=common,
        common_transactions=len(common),
        evidence=[
            (
                f"{len(common)} common "
                "counterparties detected."
            )
        ],
        metadata={
            "counterparties": list(common),
            "counterparty_count": len(common),
            "similarity": similarity,
        },
    )

    self.relationships.append(
        result
    )

    self.relationship_matrix[
        (
            wallet_a,
            wallet_b,
        )
    ] = similarity

    self.relationship_cache[
        (
            wallet_a,
            wallet_b,
        )
    ] = result

    self.statistics[
        "relationships"
    ] += 1

    self.statistics[
        "detections"
    ] += 1

    self.statistics[
        "last_run"
    ] = datetime.utcnow()

    return result

# ==========================================================
# Part 5
# Circular Flow Detection
# ==========================================================

def find_transfer_cycles(
    self,
    wallet: Optional[NodeId] = None,
    max_length: Optional[int] = None,
) -> List[List[NodeId]]:
    """
    Find circular transfer paths in the graph.

    Parameters
    ----------
    wallet
        Optional starting wallet.

    max_length
        Maximum cycle length.

    Returns
    -------
    List of transfer cycles.
    """

    max_length = (
        max_length
        or self.config.cycle_depth
    )

    cycles: List[List[NodeId]] = []

    try:

        simple_cycles = nx.simple_cycles(
            self.graph.graph
        )

        for cycle in simple_cycles:

            if len(cycle) > max_length:
                continue

            if (
                wallet is not None
                and wallet not in cycle
            ):
                continue

            cycles.append(cycle)

    except Exception:

        return []

    return cycles


def cycle_risk_score(
    self,
    cycle: List[NodeId],
) -> float:
    """
    Calculate risk score for a transfer cycle.
    """

    if len(cycle) < 2:
        return 0.0

    score = 0.0

    # Smaller cycles are generally riskier.

    score += (
        self.config.cycle_depth
        - min(
            len(cycle),
            self.config.cycle_depth,
        )
    ) / self.config.cycle_depth

    # High-risk wallets increase score.

    for node_id in cycle:

        node = self.wallet_index.get(
            node_id
        )

        if node is None:
            continue

        score += (
            node.risk_score
            / 100.0
        )

    score /= (
        len(cycle)
        + 1
    )

    return min(score, 1.0)


def detect_circular_transfers(
    self,
    wallet: Optional[NodeId] = None,
) -> List[RelationshipResult]:
    """
    Detect circular transfer relationships.
    """

    cycles = self.find_transfer_cycles(
        wallet=wallet
    )

    results: List[
        RelationshipResult
    ] = []

    for cycle in cycles:

        if len(cycle) < 2:
            continue

        score = self.cycle_risk_score(
            cycle
        )

        confidence = min(
            1.0,
            0.60 + (
                len(cycle) * 0.05
            ),
        )

        result = RelationshipResult(
            wallet_a=cycle[0],
            wallet_b=cycle[-1],
            relationship_type=RelationshipType.CIRCULAR_TRANSFER,
            score=score,
            confidence=confidence,
            risk_score=score,
            common_wallets=set(cycle),
            path_length=len(cycle),
            evidence=[
                (
                    "Circular transfer detected "
                    f"({len(cycle)} wallets)"
                )
            ],
            metadata={
                "cycle": cycle,
                "cycle_length": len(cycle),
            },
        )

        results.append(
            result
        )

        self.relationships.append(
            result
        )

        self.relationship_cache[
            (
                cycle[0],
                cycle[-1],
            )
        ] = result

        self.circular_transfer_cache[
            (
                cycle[0],
                cycle[-1],
            )
        ] = [cycle]

    self.statistics[
        "relationships"
    ] += len(results)

    self.statistics[
        "detections"
    ] += len(results)

    self.statistics[
        "last_run"
    ] = datetime.utcnow()

    return results

# ==========================================================
# Part 6A
# Hidden Relationship Detection
# Multi-hop Wallet Discovery
# ==========================================================

def find_hidden_paths(
    self,
    source: NodeId,
    target: NodeId,
    max_depth: Optional[int] = None,
    max_paths: Optional[int] = None,
) -> List[List[NodeId]]:
    """
    Discover indirect (multi-hop) paths between two wallets.

    Parameters
    ----------
    source
        Source wallet.

    target
        Destination wallet.

    max_depth
        Maximum traversal depth.

    max_paths
        Maximum number of paths returned.

    Returns
    -------
    List of wallet paths.
    """

    if source not in self.wallet_index:
        raise KeyError(
            f"Unknown wallet '{source}'."
        )

    if target not in self.wallet_index:
        raise KeyError(
            f"Unknown wallet '{target}'."
        )

    max_depth = (
        max_depth
        or self.config.max_search_depth
    )

    max_paths = (
        max_paths
        or self.config.max_paths
    )

    cache_key = (
        source,
        target,
    )

    if (
        self.config.use_cache
        and cache_key
        in self.hidden_relationship_cache
    ):
        return self.hidden_relationship_cache[
            cache_key
        ]

    paths: List[List[NodeId]] = []

    queue = deque()

    queue.append(
        (
            source,
            [source],
        )
    )

    while queue and len(paths) < max_paths:

        current, path = queue.popleft()

        if len(path) > max_depth:
            continue

        for neighbor in self.graph.graph.neighbors(
            current
        ):

            if neighbor in path:
                continue

            new_path = path + [neighbor]

            if neighbor == target:

                paths.append(new_path)

                continue

            queue.append(
                (
                    neighbor,
                    new_path,
                )
            )

    if self.config.cache_results:

        self.hidden_relationship_cache[
            cache_key
        ] = paths

    return paths


def shortest_hidden_path(
    self,
    source: NodeId,
    target: NodeId,
) -> Optional[List[NodeId]]:
    """
    Return the shortest indirect wallet path.
    """

    paths = self.find_hidden_paths(
        source,
        target,
    )

    if not paths:
        return None

    return min(
        paths,
        key=len,
    )


def hidden_path_exists(
    self,
    source: NodeId,
    target: NodeId,
) -> bool:
    """
    Determine whether an indirect
    relationship exists.
    """

    return (
        len(
            self.find_hidden_paths(
                source,
                target,
                max_paths=1,
            )
        )
        > 0
    )


def reachable_wallets(
    self,
    source: NodeId,
    depth: Optional[int] = None,
) -> WalletSet:
    """
    Return every wallet reachable
    within N hops.
    """

    depth = (
        depth
        or self.config.max_search_depth
    )

    visited: WalletSet = set()

    queue = deque()

    queue.append(
        (
            source,
            0,
        )
    )

    while queue:

        node, hops = queue.popleft()

        if hops >= depth:
            continue

        for neighbor in self.graph.graph.neighbors(
            node
        ):

            if neighbor in visited:
                continue

            visited.add(neighbor)

            queue.append(
                (
                    neighbor,
                    hops + 1,
                )
            )

    visited.discard(source)

    return visited

# ==========================================================
# Part 6B
# Indirect Funding Detection
# Funding Chain Analysis
# ==========================================================

def detect_indirect_funding(
    self,
    source: NodeId,
    target: NodeId,
    max_depth: Optional[int] = None,
) -> Optional[RelationshipResult]:
    """
    Detect whether one wallet indirectly funds another
    through intermediary wallets.
    """

    paths = self.find_hidden_paths(
        source,
        target,
        max_depth=max_depth,
    )

    if not paths:
        return None

    shortest = min(
        paths,
        key=len,
    )

    score = self.funding_chain_score(
        shortest
    )

    confidence = min(
        1.0,
        0.65 + (
            score * 0.35
        ),
    )

    intermediaries = shortest[1:-1]

    result = RelationshipResult(
        wallet_a=source,
        wallet_b=target,
        relationship_type=RelationshipType.FUNDING_CHAIN,
        score=score,
        confidence=confidence,
        risk_score=score,
        common_wallets=set(
            intermediaries
        ),
        path_length=len(shortest),
        evidence=[
            (
                f"Indirect funding chain detected "
                f"through {len(intermediaries)} "
                "intermediate wallet(s)."
            )
        ],
        metadata={
            "funding_path": shortest,
            "intermediaries": intermediaries,
            "hop_count": len(shortest) - 1,
            "path_count": len(paths),
        },
    )

    self.relationships.append(
        result
    )

    self.relationship_cache[
        (
            source,
            target,
        )
    ] = result

    self.statistics[
        "relationships"
    ] += 1

    self.statistics[
        "detections"
    ] += 1

    self.statistics[
        "last_run"
    ] = datetime.utcnow()

    return result


def funding_chain_score(
    self,
    path: List[NodeId],
) -> float:
    """
    Calculate a confidence score for an indirect
    funding chain.

    Shorter chains produce higher scores.
    """

    if len(path) < 2:
        return 0.0

    hop_count = len(path) - 1

    score = 1.0 / hop_count

    risk_bonus = 0.0

    for wallet in path:

        node = self.wallet_index.get(
            wallet
        )

        if node is None:
            continue

        risk_bonus += (
            node.risk_score / 100.0
        )

    risk_bonus /= len(path)

    score += (
        risk_bonus * 0.25
    )

    return min(
        score,
        1.0,
    )


def funding_chains(
    self,
    source: NodeId,
    target: NodeId,
    max_depth: Optional[int] = None,
) -> List[List[NodeId]]:
    """
    Return every discovered funding chain.
    """

    return self.find_hidden_paths(
        source,
        target,
        max_depth=max_depth,
    )


def shortest_funding_chain(
    self,
    source: NodeId,
    target: NodeId,
) -> Optional[List[NodeId]]:
    """
    Return the shortest funding chain.
    """

    chains = self.funding_chains(
        source,
        target,
    )

    if not chains:
        return None

    return min(
        chains,
        key=len,
    )

# ==========================================================
# Part 6D
# Hidden Ownership Chain Reconstruction
# ==========================================================

def hidden_ownership_chain(
    self,
    source: NodeId,
    target: NodeId,
    max_depth: Optional[int] = None,
) -> Optional[List[NodeId]]:
    """
    Attempt to reconstruct the most likely hidden
    ownership chain between two wallets.

    Returns the highest scoring path.
    """

    paths = self.find_hidden_paths(
        source,
        target,
        max_depth=max_depth,
    )

    if not paths:
        return None

    best_path = None
    best_score = -1.0

    for path in paths:

        score = self.ownership_chain_score(
            path,
        )

        if score > best_score:

            best_score = score

            best_path = path

    return best_path


def ownership_chain_score(
    self,
    path: List[NodeId],
) -> float:
    """
    Estimate the probability that a wallet path
    represents hidden ownership.

    Higher score = stronger ownership signal.
    """

    if len(path) < 2:
        return 0.0

    score = 0.0

    # ------------------------------------------
    # Shorter ownership chains are stronger.
    # ------------------------------------------

    hop_score = 1.0 / (
        len(path) - 1
    )

    score += hop_score * 0.35

    # ------------------------------------------
    # Funding similarity
    # ------------------------------------------

    for i in range(len(path) - 1):

        score += (
            self.shared_funding_score(
                path[i],
                path[i + 1],
            )
            * 0.20
        )

    # ------------------------------------------
    # Counterparty similarity
    # ------------------------------------------

    for i in range(len(path) - 1):

        score += (
            self.counterparty_similarity(
                path[i],
                path[i + 1],
            )
            * 0.15
        )

    # ------------------------------------------
    # Shared deployer
    # ------------------------------------------

    for i in range(len(path) - 1):

        score += (
            self.deployer_similarity(
                path[i],
                path[i + 1],
            )
            * 0.20
        )

    # ------------------------------------------
    # Risk score contribution
    # ------------------------------------------

    risk = 0.0

    for wallet in path:

        node = self.wallet_index.get(
            wallet,
        )

        if node is None:
            continue

        risk += (
            node.risk_score / 100.0
        )

    risk /= len(path)

    score += risk * 0.10

    return min(
        score,
        1.0,
    )


def ownership_chain_exists(
    self,
    source: NodeId,
    target: NodeId,
) -> bool:
    """
    Returns True if an ownership chain exists.
    """

    return (
        self.hidden_ownership_chain(
            source,
            target,
        )
        is not None
    )


def ownership_chain_confidence(
    self,
    source: NodeId,
    target: NodeId,
) -> float:
    """
    Confidence of the reconstructed ownership chain.
    """

    chain = self.hidden_ownership_chain(
        source,
        target,
    )

    if chain is None:
        return 0.0

    return self.ownership_chain_score(
        chain,
    )


def ownership_chain_relationship(
    self,
    source: NodeId,
    target: NodeId,
) -> Optional[RelationshipResult]:
    """
    Produce a RelationshipResult describing the
    reconstructed ownership chain.
    """

    chain = self.hidden_ownership_chain(
        source,
        target,
    )

    if chain is None:
        return None

    score = self.ownership_chain_score(
        chain,
    )

    result = RelationshipResult(
        wallet_a=source,
        wallet_b=target,
        relationship_type=RelationshipType.MULTI_WALLET_OWNER,
        score=score,
        confidence=score,
        risk_score=score,
        common_wallets=set(chain[1:-1]),
        path_length=len(chain),
        evidence=[
            (
                "Likely hidden ownership chain "
                f"through {len(chain)-2} intermediary wallet(s)."
            )
        ],
        metadata={
            "ownership_chain": chain,
            "chain_length": len(chain),
            "ownership_probability": score,
        },
    )

    self.relationships.append(
        result
    )

    self.relationship_cache[
        (
            source,
            target,
        )
    ] = result

    self.statistics[
        "relationships"
    ] += 1

    self.statistics[
        "detections"
    ] += 1

    self.statistics[
        "last_run"
    ] = datetime.utcnow()

    return result

# ==========================================================
# Part 7A
# Cluster Detection
# ==========================================================

def cluster_wallets(
    self,
    wallet: NodeId,
) -> WalletCluster:
    """
    Build a wallet cluster starting from one wallet.

    Relationships considered:

    • Shared funding
    • Shared deployer
    • Hidden ownership
    • Common counterparties
    """

    if wallet not in self.wallet_index:
        raise KeyError(
            f"Unknown wallet '{wallet}'."
        )

    cluster: WalletCluster = set()

    queue = deque([wallet])

    while queue:

        current = queue.popleft()

        if current in cluster:
            continue

        cluster.add(current)

        for other in self.wallet_index.keys():

            if other == current:
                continue

            if other in cluster:
                continue

            score = self.same_owner_probability(
                current,
                other,
            )

            if (
                score
                >= self.config.relationship_threshold
            ):

                queue.append(other)

    return cluster


def merge_clusters(
    self,
    clusters: WalletClusters,
) -> WalletClusters:
    """
    Merge overlapping wallet clusters.
    """

    merged: WalletClusters = []

    while clusters:

        current = clusters.pop()

        changed = True

        while changed:

            changed = False

            remaining = []

            for other in clusters:

                if current.intersection(other):

                    current |= other

                    changed = True

                else:

                    remaining.append(other)

            clusters = remaining

        merged.append(current)

    return merged


def detect_wallet_clusters(
    self,
) -> WalletClusters:
    """
    Detect clusters of wallets likely
    controlled by the same owner.
    """

    visited: WalletSet = set()

    clusters: WalletClusters = []

    for wallet in self.wallet_index.keys():

        if wallet in visited:
            continue

        cluster = self.cluster_wallets(
            wallet,
        )

        if len(cluster) <= 1:
            continue

        visited.update(cluster)

        clusters.append(cluster)

    clusters = self.merge_clusters(
        clusters,
    )

    self.wallet_clusters = clusters

    self.statistics[
        "clusters"
    ] = len(clusters)

    self.statistics[
        "last_run"
    ] = datetime.utcnow()

    return clusters

# ==========================================================
# Part 7B
# Ownership Scoring
# ==========================================================

def ownership_score(
    self,
    wallet_a: NodeId,
    wallet_b: NodeId,
) -> float:
    """
    Composite ownership score.

    Combines every ownership signal into
    a normalized score between 0 and 1.
    """

    funding = self.shared_funding_score(
        wallet_a,
        wallet_b,
    )

    deployer = self.deployer_similarity(
        wallet_a,
        wallet_b,
    )

    counterparty = self.counterparty_similarity(
        wallet_a,
        wallet_b,
    )

    intermediary = self.intermediary_similarity(
        wallet_a,
        wallet_b,
    )

    ownership = 0.0

    chain = self.hidden_ownership_chain(
        wallet_a,
        wallet_b,
    )

    if chain is not None:

        ownership = self.ownership_chain_score(
            chain
        )

    score = (
        funding * 0.30
        + deployer * 0.25
        + counterparty * 0.15
        + intermediary * 0.15
        + ownership * 0.15
    )

    return min(
        score,
        1.0,
    )


def cluster_confidence(
    self,
    cluster: WalletCluster,
) -> float:
    """
    Calculate confidence that an entire cluster
    belongs to one owner.
    """

    wallets = list(cluster)

    if len(wallets) <= 1:
        return 0.0

    scores: List[float] = []

    for i in range(len(wallets)):

        for j in range(i + 1, len(wallets)):

            scores.append(
                self.ownership_score(
                    wallets[i],
                    wallets[j],
                )
            )

    if not scores:
        return 0.0

    return sum(scores) / len(scores)


def same_owner_probability(
    self,
    wallet_a: NodeId,
    wallet_b: NodeId,
) -> float:
    """
    Probability that two wallets belong
    to the same owner.
    """

    cache_key = (
        wallet_a,
        wallet_b,
    )

    if (
        self.config.use_cache
        and cache_key in self.similarity_cache
    ):
        return self.similarity_cache[
            cache_key
        ]

    probability = self.ownership_score(
        wallet_a,
        wallet_b,
    )

    if self.config.cache_results:

        self.similarity_cache[
            cache_key
        ] = probability

    return probability                

# ==========================================================
# Part 7C
# Device / IP Heuristic Hooks
#
# NOTE:
# Solana blockchain DOES NOT expose:
#
# • Device IDs
# • IP Addresses
# • Browser fingerprints
#
# These methods are hook points for future
# Sentinel AI Enterprise integrations.
# ==========================================================

def device_fingerprint_score(
    self,
    wallet_a: NodeId,
    wallet_b: NodeId,
    *,
    device_id_a: Optional[str] = None,
    device_id_b: Optional[str] = None,
) -> float:
    """
    Device fingerprint similarity.

    Future integrations:
    • Sentinel Desktop
    • Sentinel Mobile
    • OAuth Providers
    • Exchange APIs
    """

    if device_id_a is None:
        return 0.0

    if device_id_b is None:
        return 0.0

    if device_id_a == device_id_b:
        return 1.0

    return 0.0


def ip_similarity_score(
    self,
    wallet_a: NodeId,
    wallet_b: NodeId,
    *,
    ip_a: Optional[str] = None,
    ip_b: Optional[str] = None,
) -> float:
    """
    IP similarity.

    Placeholder hook.

    Future integrations:
    • Exchange KYC
    • Sentinel Enterprise
    • Internal telemetry
    """

    if ip_a is None:
        return 0.0

    if ip_b is None:
        return 0.0

    if ip_a == ip_b:
        return 1.0

    return 0.0


def browser_fingerprint_score(
    self,
    wallet_a: NodeId,
    wallet_b: NodeId,
    *,
    fingerprint_a: Optional[str] = None,
    fingerprint_b: Optional[str] = None,
) -> float:
    """
    Browser fingerprint similarity.

    Placeholder hook.

    Future integrations:

    • Chromium Fingerprint
    • Canvas Fingerprint
    • WebGL Fingerprint
    • TLS Fingerprint
    """

    if fingerprint_a is None:
        return 0.0

    if fingerprint_b is None:
        return 0.0

    if fingerprint_a == fingerprint_b:
        return 1.0

    return 0.0


def offchain_identity_score(
    self,
    wallet_a: NodeId,
    wallet_b: NodeId,
    *,
    device_score: float = 0.0,
    ip_score: float = 0.0,
    browser_score: float = 0.0,
) -> float:
    """
    Composite off-chain identity score.

    This score is NOT used unless external
    telemetry is available.
    """

    score = (
        device_score * 0.45
        + ip_score * 0.35
        + browser_score * 0.20
    )

    return min(
        score,
        1.0,
    )

# ==========================================================
# Part 7D
# Funding Heuristics
# ==========================================================

def funding_similarity_score(
    self,
    wallet_a: NodeId,
    wallet_b: NodeId,
) -> float:
    """
    Calculate funding similarity using multiple
    funding-related heuristics.

    Returns
    -------
    float
        Normalized similarity score (0.0 - 1.0).
    """

    shared_funding = self.shared_funding_score(
        wallet_a,
        wallet_b,
    )

    indirect_funding = 0.0

    funding_result = self.detect_indirect_funding(
        wallet_a,
        wallet_b,
    )

    if funding_result is not None:
        indirect_funding = funding_result.score

    score = (
        shared_funding * 0.70
        + indirect_funding * 0.30
    )

    return min(score, 1.0)


def same_funder_probability(
    self,
    wallet_a: NodeId,
    wallet_b: NodeId,
) -> float:
    """
    Probability that two wallets share
    the same funding source.
    """

    cache_key = (
        wallet_a,
        wallet_b,
        "same_funder",
    )

    if (
        self.config.use_cache
        and cache_key
        in self.relationship_cache
    ):
        cached = self.relationship_cache[
            cache_key
        ]

        if isinstance(
            cached,
            (int, float),
        ):
            return float(cached)

    probability = self.funding_similarity_score(
        wallet_a,
        wallet_b,
    )

    if self.config.cache_results:

        self.relationship_cache[
            cache_key
        ] = probability

    return probability


def funding_cluster_score(
    self,
    cluster: WalletCluster,
) -> float:
    """
    Calculate funding consistency across an
    entire wallet cluster.
    """

    wallets = list(cluster)

    if len(wallets) <= 1:
        return 0.0

    scores: List[float] = []

    for i in range(len(wallets)):

        for j in range(i + 1, len(wallets)):

            scores.append(
                self.funding_similarity_score(
                    wallets[i],
                    wallets[j],
                )
            )

    if not scores:
        return 0.0

    return sum(scores) / len(scores)

# ==========================================================
# Part 7E
# Behavioral Similarity
# ==========================================================

def token_overlap_similarity(
    self,
    wallet_a: NodeId,
    wallet_b: NodeId,
) -> float:
    """
    Compare token portfolios using Jaccard similarity.
    """

    node_a = self.wallet_index.get(wallet_a)
    node_b = self.wallet_index.get(wallet_b)

    if node_a is None or node_b is None:
        return 0.0

    tokens_a = set(
        node_a.metadata.get(
            "tokens",
            [],
        )
    )

    tokens_b = set(
        node_b.metadata.get(
            "tokens",
            [],
        )
    )

    if not tokens_a and not tokens_b:
        return 0.0

    union = tokens_a | tokens_b

    if not union:
        return 0.0

    return len(tokens_a & tokens_b) / len(union)


def timing_similarity(
    self,
    wallet_a: NodeId,
    wallet_b: NodeId,
) -> float:
    """
    Compare wallet activity timing.
    """

    node_a = self.wallet_index.get(wallet_a)
    node_b = self.wallet_index.get(wallet_b)

    if node_a is None or node_b is None:
        return 0.0

    delta = abs(
        (
            node_a.last_seen
            - node_b.last_seen
        ).total_seconds()
    )

    one_day = 86400

    score = max(
        0.0,
        1.0 - (delta / one_day),
    )

    return score


def trading_pattern_similarity(
    self,
    wallet_a: NodeId,
    wallet_b: NodeId,
) -> float:
    """
    Compare trading characteristics.
    """

    node_a = self.wallet_index.get(wallet_a)
    node_b = self.wallet_index.get(wallet_b)

    if node_a is None or node_b is None:
        return 0.0

    tx_similarity = 1.0 - (
        abs(
            node_a.tx_count
            - node_b.tx_count
        )
        /
        max(
            node_a.tx_count,
            node_b.tx_count,
            1,
        )
    )

    token_similarity = 1.0 - (
        abs(
            node_a.token_count
            - node_b.token_count
        )
        /
        max(
            node_a.token_count,
            node_b.token_count,
            1,
        )
    )

    balance_similarity = 1.0 - (
        abs(
            node_a.balance_sol
            - node_b.balance_sol
        )
        /
        max(
            node_a.balance_sol,
            node_b.balance_sol,
            1.0,
        )
    )

    return (
        tx_similarity * 0.40
        + token_similarity * 0.30
        + balance_similarity * 0.30
    )


def behavior_similarity(
    self,
    wallet_a: NodeId,
    wallet_b: NodeId,
) -> float:
    """
    Overall behavioral similarity score.
    """

    trading = self.trading_pattern_similarity(
        wallet_a,
        wallet_b,
    )

    timing = self.timing_similarity(
        wallet_a,
        wallet_b,
    )

    token_overlap = self.token_overlap_similarity(
        wallet_a,
        wallet_b,
    )

    funding = self.funding_similarity_score(
        wallet_a,
        wallet_b,
    )

    score = (
        trading * 0.35
        + timing * 0.20
        + token_overlap * 0.20
        + funding * 0.25
    )

    return min(score, 1.0)

# ==========================================================
# Part 7F
# Composite Multi-Wallet Ownership Engine
# ==========================================================

def detect_multi_wallet_ownership(
    self,
    wallet_a: NodeId,
    wallet_b: NodeId,
) -> Optional[RelationshipResult]:
    """
    Detect whether two wallets are likely owned by
    the same entity using every ownership heuristic.
    """

    probability = self.same_owner_probability(
        wallet_a,
        wallet_b,
    )

    if (
        probability
        < self.config.relationship_threshold
    ):
        return None

    cluster = self.cluster_wallets(
        wallet_a,
    )

    cluster_conf = self.cluster_confidence(
        cluster,
    )

    funding_score = self.funding_similarity_score(
        wallet_a,
        wallet_b,
    )

    behavior_score = self.behavior_similarity(
        wallet_a,
        wallet_b,
    )

    deployer_score = self.deployer_similarity(
        wallet_a,
        wallet_b,
    )

    ownership_chain = self.hidden_ownership_chain(
        wallet_a,
        wallet_b,
    )

    confidence = (
        probability * 0.50
        + cluster_conf * 0.20
        + funding_score * 0.10
        + behavior_score * 0.10
        + deployer_score * 0.10
    )

    confidence = min(
        confidence,
        1.0,
    )

    evidence: List[str] = []

    if funding_score > 0:
        evidence.append(
            "Shared funding detected."
        )

    if deployer_score > 0:
        evidence.append(
            "Shared deployer."
        )

    if behavior_score > 0:
        evidence.append(
            "Behavioral similarity."
        )

    if ownership_chain is not None:
        evidence.append(
            "Ownership chain reconstructed."
        )

    evidence.append(
        f"Cluster size: {len(cluster)}"
    )

    result = RelationshipResult(
        wallet_a=wallet_a,
        wallet_b=wallet_b,
        relationship_type=RelationshipType.MULTI_WALLET_OWNER,
        score=probability,
        confidence=confidence,
        risk_score=probability,
        common_wallets=cluster - {
            wallet_a,
            wallet_b,
        },
        common_transactions=0,
        path_length=(
            len(ownership_chain)
            if ownership_chain
            else None
        ),
        evidence=evidence,
        metadata={
            "cluster": list(cluster),
            "cluster_size": len(cluster),
            "cluster_confidence": cluster_conf,
            "ownership_probability": probability,
            "funding_score": funding_score,
            "behavior_score": behavior_score,
            "deployer_score": deployer_score,
            "ownership_chain": ownership_chain,
        },
    )

    cache_key = (
        wallet_a,
        wallet_b,
    )

    # ------------------------------------------
    # Relationship Storage
    # ------------------------------------------

    self.relationships.append(
        result,
    )

    self.relationship_matrix[
        cache_key
    ] = probability

    # ------------------------------------------
    # Cache Updates
    # ------------------------------------------

    self.relationship_cache[
        cache_key
    ] = result

    self.similarity_cache[
        cache_key
    ] = probability

    self.wallet_clusters = self.merge_clusters(
        self.wallet_clusters + [cluster]
    )

    # ------------------------------------------
    # Statistics
    # ------------------------------------------

    self.statistics[
        "relationships"
    ] += 1

    self.statistics[
        "detections"
    ] += 1

    self.statistics[
        "clusters"
    ] = len(
        self.wallet_clusters
    )

    self.statistics[
        "last_run"
    ] = datetime.utcnow()

    return result

# ==========================================================
# Part 8A
# Composite Relationship Scoring
# ==========================================================

def relationship_components(
    self,
    wallet_a: NodeId,
    wallet_b: NodeId,
) -> Dict[str, float]:
    """
    Return every component contributing to the final
    relationship score.
    """

    funding = self.funding_similarity_score(
        wallet_a,
        wallet_b,
    )

    deployer = self.deployer_similarity(
        wallet_a,
        wallet_b,
    )

    counterparty = self.counterparty_similarity(
        wallet_a,
        wallet_b,
    )

    intermediary = self.intermediary_similarity(
        wallet_a,
        wallet_b,
    )

    behavior = self.behavior_similarity(
        wallet_a,
        wallet_b,
    )

    ownership = self.same_owner_probability(
        wallet_a,
        wallet_b,
    )

    hidden = 0.0

    hidden_result = self.detect_hidden_relationship(
        wallet_a,
        wallet_b,
    )

    if hidden_result is not None:
        hidden = hidden_result.score

    return {
        "funding": funding,
        "deployer": deployer,
        "counterparty": counterparty,
        "intermediary": intermediary,
        "behavior": behavior,
        "ownership": ownership,
        "hidden_relationship": hidden,
    }


def overall_relationship_score(
    self,
    wallet_a: NodeId,
    wallet_b: NodeId,
) -> float:
    """
    Calculate the overall relationship score between
    two wallets.

    Returns a normalized score between 0 and 1.
    """

    components = self.relationship_components(
        wallet_a,
        wallet_b,
    )

    weights = {
        "funding": 0.22,
        "deployer": 0.15,
        "counterparty": 0.13,
        "intermediary": 0.10,
        "behavior": 0.15,
        "ownership": 0.15,
        "hidden_relationship": 0.10,
    }

    score = 0.0

    for key, weight in weights.items():

        score += (
            components.get(key, 0.0)
            * weight
        )

    return min(
        max(score, 0.0),
        1.0,
    )

# ==========================================================
# Part 8B
# Confidence & Risk Calculation
# ==========================================================

def relationship_confidence(
    self,
    wallet_a: NodeId,
    wallet_b: NodeId,
) -> float:
    """
    Calculate confidence in the detected relationship.

    Confidence measures how much independent evidence
    supports the relationship.
    """

    components = self.relationship_components(
        wallet_a,
        wallet_b,
    )

    score = self.overall_relationship_score(
        wallet_a,
        wallet_b,
    )

    active_components = sum(
        1
        for value in components.values()
        if value >= 0.30
    )

    evidence_factor = (
        active_components
        / max(len(components), 1)
    )

    variance = statistics.pvariance(
        list(components.values())
    )

    consistency = max(
        0.0,
        1.0 - variance,
    )

    confidence = (
        score * 0.50
        + evidence_factor * 0.30
        + consistency * 0.20
    )

    return min(
        max(confidence, 0.0),
        1.0,
    )


def relationship_risk_score(
    self,
    wallet_a: NodeId,
    wallet_b: NodeId,
) -> float:
    """
    Estimate relationship risk.

    Higher values indicate stronger likelihood
    of coordinated or suspicious activity.
    """

    node_a = self.wallet_index.get(
        wallet_a,
    )

    node_b = self.wallet_index.get(
        wallet_b,
    )

    if node_a is None or node_b is None:
        return 0.0

    relationship_score = (
        self.overall_relationship_score(
            wallet_a,
            wallet_b,
        )
    )

    ownership_score = (
        self.same_owner_probability(
            wallet_a,
            wallet_b,
        )
    )

    funding_score = (
        self.funding_similarity_score(
            wallet_a,
            wallet_b,
        )
    )

    hidden_score = 0.0

    hidden = self.detect_hidden_relationship(
        wallet_a,
        wallet_b,
    )

    if hidden is not None:
        hidden_score = hidden.score

    wallet_risk = (
        node_a.risk_score
        + node_b.risk_score
    ) / 200.0

    risk = (
        relationship_score * 0.30
        + ownership_score * 0.25
        + funding_score * 0.15
        + hidden_score * 0.15
        + wallet_risk * 0.15
    )

    return min(
        max(risk, 0.0),
        1.0,
    )

# ==========================================================
# Part 8C
# AI Explanation Generator
# ==========================================================

def explain_relationship(
    self,
    wallet_a: NodeId,
    wallet_b: NodeId,
) -> str:
    """
    Generate a human-readable explanation describing
    why two wallets are considered related.
    """

    components = self.relationship_components(
        wallet_a,
        wallet_b,
    )

    confidence = self.relationship_confidence(
        wallet_a,
        wallet_b,
    )

    risk = self.relationship_risk_score(
        wallet_a,
        wallet_b,
    )

    overall = self.overall_relationship_score(
        wallet_a,
        wallet_b,
    )

    reasons: List[str] = []

    if components["funding"] >= 0.50:
        reasons.append(
            "shared funding sources"
        )

    if components["deployer"] >= 0.50:
        reasons.append(
            "same deployer"
        )

    if components["counterparty"] >= 0.50:
        reasons.append(
            "common counterparties"
        )

    if components["intermediary"] >= 0.50:
        reasons.append(
            "shared intermediary wallets"
        )

    if components["behavior"] >= 0.50:
        reasons.append(
            "similar trading behavior"
        )

    if components["ownership"] >= 0.50:
        reasons.append(
            "multi-wallet ownership indicators"
        )

    if components["hidden_relationship"] >= 0.50:
        reasons.append(
            "hidden ownership chain"
        )

    if not reasons:
        reasons.append(
            "weak behavioral similarity"
        )

    explanation = (
        f"Wallets {wallet_a} and {wallet_b} "
        f"have an overall relationship score of "
        f"{overall:.2f} with confidence "
        f"{confidence:.2f} and risk score "
        f"{risk:.2f}. "
        f"The strongest indicators are "
        + ", ".join(reasons)
        + "."
    )

    return explanation


def relationship_summary(
    self,
    wallet_a: NodeId,
    wallet_b: NodeId,
) -> Dict[str, Any]:
    """
    Generate a structured AI-friendly summary.
    """

    components = self.relationship_components(
        wallet_a,
        wallet_b,
    )

    return {
        "wallet_a": wallet_a,
        "wallet_b": wallet_b,
        "overall_score": self.overall_relationship_score(
            wallet_a,
            wallet_b,
        ),
        "confidence": self.relationship_confidence(
            wallet_a,
            wallet_b,
        ),
        "risk_score": self.relationship_risk_score(
            wallet_a,
            wallet_b,
        ),
        "components": components,
        "explanation": self.explain_relationship(
            wallet_a,
            wallet_b,
        ),
    }

# ==========================================================
# Part 8D
# Export Methods
# ==========================================================

def export_relationship(
    self,
    relationship: RelationshipResult,
) -> Dict[str, Any]:
    """
    Export a single RelationshipResult as a dictionary.
    """

    return {
        "wallet_a": relationship.wallet_a,
        "wallet_b": relationship.wallet_b,
        "relationship_type": relationship.relationship_type.value,
        "score": relationship.score,
        "confidence": relationship.confidence,
        "risk_score": relationship.risk_score,
        "common_wallets": list(
            relationship.common_wallets
        ),
        "common_transactions": relationship.common_transactions,
        "path_length": relationship.path_length,
        "evidence": relationship.evidence,
        "metadata": relationship.metadata,
    }


def export_relationships(
    self,
) -> List[Dict[str, Any]]:
    """
    Export every detected relationship.
    """

    return [
        self.export_relationship(r)
        for r in self.relationships
    ]


def to_dataframe(
    self,
) -> "pd.DataFrame":
    """
    Export relationships as a pandas DataFrame.
    """

    try:
        import pandas as pd

    except ImportError as exc:
        raise ImportError(
            "pandas is required for DataFrame export."
        ) from exc

    return pd.DataFrame(
        self.export_relationships()
    )


def to_json(
    self,
    *,
    indent: int = 4,
) -> str:
    """
    Export relationships to JSON string.
    """

    return json.dumps(
        self.export_relationships(),
        indent=indent,
        default=str,
    )


def save_json(
    self,
    filepath: Union[str, Path],
    *,
    indent: int = 4,
) -> None:
    """
    Save relationships to a JSON file.
    """

    filepath = Path(filepath)

    filepath.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with filepath.open(
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            self.export_relationships(),
            f,
            indent=indent,
            default=str,
        )


def to_csv(
    self,
    filepath: Union[str, Path],
) -> None:
    """
    Export relationships to CSV.
    """

    df = self.to_dataframe()

    df.to_csv(
        filepath,
        index=False,
    )

# ==========================================================
# Part 8E
# Analytics & Rankings
# ==========================================================

def top_relationships(
    self,
    limit: int = 20,
) -> List[RelationshipResult]:
    """
    Return the strongest relationships ranked by
    overall relationship score.
    """

    return sorted(
        self.relationships,
        key=lambda r: r.score,
        reverse=True,
    )[:limit]


def high_risk_relationships(
    self,
    min_risk: float = 0.70,
    limit: Optional[int] = None,
) -> List[RelationshipResult]:
    """
    Return relationships whose risk score exceeds
    the specified threshold.
    """

    relationships = [
        r
        for r in self.relationships
        if r.risk_score >= min_risk
    ]

    relationships.sort(
        key=lambda r: (
            r.risk_score,
            r.confidence,
        ),
        reverse=True,
    )

    if limit is not None:
        relationships = relationships[:limit]

    return relationships


def relationship_statistics(
    self,
) -> Dict[str, Any]:
    """
    Generate analytics for all detected relationships.
    """

    if not self.relationships:

        return {
            "total_relationships": 0,
            "average_score": 0.0,
            "average_confidence": 0.0,
            "average_risk": 0.0,
            "max_score": 0.0,
            "max_risk": 0.0,
            "relationship_types": {},
            "clusters": len(
                self.wallet_clusters
            ),
        }

    total = len(
        self.relationships
    )

    avg_score = (
        sum(
            r.score
            for r in self.relationships
        )
        / total
    )

    avg_confidence = (
        sum(
            r.confidence
            for r in self.relationships
        )
        / total
    )

    avg_risk = (
        sum(
            r.risk_score
            for r in self.relationships
        )
        / total
    )

    max_score = max(
        r.score
        for r in self.relationships
    )

    max_risk = max(
        r.risk_score
        for r in self.relationships
    )

    type_counts: Dict[
        str,
        int,
    ] = defaultdict(int)

    for relationship in self.relationships:

        type_counts[
            relationship.relationship_type.value
        ] += 1

    return {
        "total_relationships": total,
        "average_score": round(
            avg_score,
            4,
        ),
        "average_confidence": round(
            avg_confidence,
            4,
        ),
        "average_risk": round(
            avg_risk,
            4,
        ),
        "max_score": round(
            max_score,
            4,
        ),
        "max_risk": round(
            max_risk,
            4,
        ),
        "relationship_types": dict(
            type_counts
        ),
        "clusters": len(
            self.wallet_clusters
        ),
        "cache_size": len(
            self.relationship_cache
        ),
        "matrix_size": len(
            self.relationship_matrix
        ),
        "statistics": dict(
            self.statistics
        ),
    }        

# ==========================================================
# Part 8F
# Relationship Engine Entry Point
# ==========================================================

def analyze_relationship(
    self,
    wallet_a: NodeId,
    wallet_b: NodeId,
    *,
    refresh_cache: bool = True,
) -> Optional[RelationshipResult]:
    """
    Run the complete relationship engine between
    two wallets.

    Pipeline

    1. Refresh caches
    2. Composite relationship score
    3. Confidence
    4. Risk
    5. AI explanation
    6. RelationshipResult
    """

    cache_key = (wallet_a, wallet_b)

    # --------------------------------------------------
    # Cache refresh
    # --------------------------------------------------

    if refresh_cache:

        self.relationship_cache.pop(
            cache_key,
            None,
        )

        self.similarity_cache.pop(
            cache_key,
            None,
        )

        self.relationship_matrix.pop(
            cache_key,
            None,
        )

    # --------------------------------------------------
    # Scores
    # --------------------------------------------------

    overall_score = self.overall_relationship_score(
        wallet_a,
        wallet_b,
    )

    if overall_score < self.config.relationship_threshold:
        return None

    confidence = self.relationship_confidence(
        wallet_a,
        wallet_b,
    )

    risk = self.relationship_risk_score(
        wallet_a,
        wallet_b,
    )

    explanation = self.explain_relationship(
        wallet_a,
        wallet_b,
    )

    components = self.relationship_components(
        wallet_a,
        wallet_b,
    )

    relationship = RelationshipResult(
        wallet_a=wallet_a,
        wallet_b=wallet_b,
        relationship_type=RelationshipType.HIDDEN_RELATIONSHIP,
        score=overall_score,
        confidence=confidence,
        risk_score=risk,
        common_wallets=self.shared_intermediaries(
            wallet_a,
            wallet_b,
        ),
        common_transactions=0,
        path_length=None,
        evidence=[explanation],
        metadata={
            "components": components,
            "analysis_time": datetime.utcnow().isoformat(),
        },
    )

    # --------------------------------------------------
    # Cache updates
    # --------------------------------------------------

    self.relationship_cache[
        cache_key
    ] = relationship

    self.similarity_cache[
        cache_key
    ] = overall_score

    self.relationship_matrix[
        cache_key
    ] = overall_score

    # Replace existing relationship if present
    self.relationships = [
        r
        for r in self.relationships
        if not (
            r.wallet_a == wallet_a
            and r.wallet_b == wallet_b
        )
    ]

    self.relationships.append(
        relationship
    )

    # --------------------------------------------------
    # Statistics
    # --------------------------------------------------

    self.statistics["analyses"] = (
        self.statistics.get(
            "analyses",
            0,
        )
        + 1
    )

    self.statistics["last_analysis"] = (
        datetime.utcnow()
    )

    self.statistics["relationships"] = len(
        self.relationships
    )

    self.statistics["cache_size"] = len(
        self.relationship_cache
    )

    return relationship


def analyze_all_relationships(
    self,
    *,
    refresh_cache: bool = True,
) -> List[RelationshipResult]:
    """
    Analyze every wallet pair in the graph.

    Returns all detected relationships.
    """

    wallets = list(
        self.wallet_index.keys()
    )

    results: List[
        RelationshipResult
    ] = []

    # --------------------------------------------------
    # Optional cache refresh
    # --------------------------------------------------

    if refresh_cache:

        self.relationship_cache.clear()

        self.similarity_cache.clear()

        self.relationship_matrix.clear()

    # --------------------------------------------------
    # Analyze every pair
    # --------------------------------------------------

    for i in range(len(wallets)):

        for j in range(i + 1, len(wallets)):

            relationship = self.analyze_relationship(
                wallets[i],
                wallets[j],
                refresh_cache=False,
            )

            if relationship is not None:

                results.append(
                    relationship
                )

    # --------------------------------------------------
    # Update clusters
    # --------------------------------------------------

    self.detect_wallet_clusters()

    # --------------------------------------------------
    # Final statistics
    # --------------------------------------------------

    self.statistics["wallets"] = len(
        wallets
    )

    self.statistics["relationships"] = len(
        results
    )

    self.statistics["clusters"] = len(
        self.wallet_clusters
    )

    self.statistics["cache_size"] = len(
        self.relationship_cache
    )

    self.statistics["matrix_size"] = len(
        self.relationship_matrix
    )

    self.statistics["last_full_analysis"] = (
        datetime.utcnow()
    )

    return results