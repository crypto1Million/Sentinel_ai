# ==========================================================
# Part 1
# Imports
# Constants
# Enums
# Type Aliases
# GraphNode
# GraphEdge
# FundingGraph
# GraphConfig
# ==========================================================

from __future__ import annotations

import hashlib
import logging
import statistics
import time

from collections import defaultdict

from dataclasses import (
    dataclass,
    field,
)

from datetime import datetime

from enum import Enum

from pathlib import Path

from typing import (
    Any,
    DefaultDict,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
    TypeAlias,
)

# ==========================================================
# Internal Imports
# ==========================================================

from sentinel.blockchain.transaction_fetcher import (
    TransactionFetcher,
    TransactionRecord,
)

# ==========================================================
# Constants
# ==========================================================

DEFAULT_CACHE_TTL = 600

DEFAULT_MAX_DEPTH = 20

DEFAULT_EDGE_WEIGHT = 1.0

DEFAULT_MIN_TRANSFER_SOL = 0.001

DEFAULT_MAX_NEIGHBORS = 1000

DEFAULT_BATCH_SIZE = 100

# ==========================================================
# Enums
# ==========================================================

class NodeType(Enum):
    """
    Graph node types.
    """

    WALLET = "wallet"

    EXCHANGE = "exchange"

    BRIDGE = "bridge"

    TOKEN = "token"

    NFT = "nft"

    PROGRAM = "program"

    UNKNOWN = "unknown"


class EdgeType(Enum):
    """
    Funding graph edge types.
    """

    FUNDING = "funding"

    TOKEN_TRANSFER = "token_transfer"

    SOL_TRANSFER = "sol_transfer"

    SWAP = "swap"

    MINT = "mint"

    BURN = "burn"

    LIQUIDITY = "liquidity"

    STAKE = "stake"

    PROGRAM_INTERACTION = (
        "program_interaction"
    )


class GraphStatus(Enum):

    EMPTY = "empty"

    BUILDING = "building"

    READY = "ready"

    ERROR = "error"


# ==========================================================
# Type Aliases
# ==========================================================

WalletAddress: TypeAlias = str

TokenMint: TypeAlias = str

ProgramID: TypeAlias = str

Signature: TypeAlias = str

NodeID: TypeAlias = str

JSONDict: TypeAlias = Dict[str, Any]

# ==========================================================
# Graph Node
# ==========================================================

@dataclass(slots=True)
class GraphNode:
    """
    A node within the funding graph.
    """

    id: NodeID

    node_type: NodeType

    label: Optional[str] = None

    metadata: JSONDict = field(
        default_factory=dict
    )

    first_seen: Optional[
        datetime
    ] = None

    last_seen: Optional[
        datetime
    ] = None

    risk_score: float = 0.0

    confidence: float = 1.0


# ==========================================================
# Graph Edge
# ==========================================================

@dataclass(slots=True)
class GraphEdge:
    """
    Directed relationship between
    two graph nodes.
    """

    source: NodeID

    target: NodeID

    edge_type: EdgeType

    signature: Optional[
        Signature
    ] = None

    timestamp: Optional[
        int
    ] = None

    slot: Optional[
        int
    ] = None

    amount: float = 0.0

    token_mint: Optional[
        TokenMint
    ] = None

    program_id: Optional[
        ProgramID
    ] = None

    weight: float = (
        DEFAULT_EDGE_WEIGHT
    )

    confidence: float = 1.0

    metadata: JSONDict = field(
        default_factory=dict)


# ==========================================================
# Funding Graph
# ==========================================================

@dataclass(slots=True)
class FundingGraph:
    """
    Canonical graph representation used
    by FundingTracker, ClusterEngine,
    WalletSimilarity and RelationshipEngine.
    """

    nodes: Dict[
        NodeID,
        GraphNode,
    ] = field(
        default_factory=dict
    )

    edges: List[
        GraphEdge
    ] = field(
        default_factory=list
    )

    adjacency: DefaultDict[
        NodeID,
        Set[NodeID],
    ] = field(
        default_factory=lambda:
        defaultdict(set)
    )

    reverse_adjacency: DefaultDict[
        NodeID,
        Set[NodeID],
    ] = field(
        default_factory=lambda:
        defaultdict(set)
    )

    status: GraphStatus = (
        GraphStatus.EMPTY
    )

    created_at: datetime = field(
        default_factory=datetime.utcnow
    )

    updated_at: datetime = field(
        default_factory=datetime.utcnow
    )


# ==========================================================
# Graph Configuration
# ==========================================================

@dataclass(slots=True)
class GraphConfig:
    """
    FundingGraphBuilder configuration.
    """

    cache_ttl: int = (
        DEFAULT_CACHE_TTL
    )

    batch_size: int = (
        DEFAULT_BATCH_SIZE
    )

    max_depth: int = (
        DEFAULT_MAX_DEPTH
    )

    min_transfer_sol: float = (
        DEFAULT_MIN_TRANSFER_SOL
    )

    max_neighbors: int = (
        DEFAULT_MAX_NEIGHBORS
    )

    build_token_edges: bool = True

    build_program_edges: bool = True

    build_nft_edges: bool = True

    build_bridge_edges: bool = True

    build_exchange_edges: bool = True

    weighted_graph: bool = True

    update_indexes: bool = True

    save_on_build: bool = True

# ==========================================================
# Part 2
# Initialization
# Internal Graph
# Cache
# Statistics
# ==========================================================

class FundingGraphBuilder:
    """
    Builds and maintains Sentinel AI's
    canonical funding graph.

    Every analysis engine (FundingTracker,
    WalletSimilarity, RelationshipDetector,
    ClusterEngine, WalletDNA, RugRadar, etc.)
    should consume this graph instead of
    querying Helius directly.
    """

    # ======================================================
    # Initialization
    # ======================================================

    def __init__(
        self,
        transaction_fetcher: TransactionFetcher,
        *,
        config: Optional[
            GraphConfig
        ] = None,
    ) -> None:

        self.config = (
            config
            or GraphConfig()
        )

        self.fetcher = (
            transaction_fetcher
        )

        self.logger = logging.getLogger(
            self.__class__.__name__
        )

        # ==================================================
        # Internal Graph
        # ==================================================

        self.graph = FundingGraph()

        # Node indexes

        self.nodes: Dict[
            NodeID,
            GraphNode,
        ] = self.graph.nodes

        self.edges: List[
            GraphEdge
        ] = self.graph.edges

        self.adjacency = (
            self.graph.adjacency
        )

        self.reverse_adjacency = (
            self.graph.reverse_adjacency
        )

        # Fast lookup indexes

        self.wallet_index: Dict[
            WalletAddress,
            GraphNode,
        ] = {}

        self.exchange_index: Dict[
            WalletAddress,
            GraphNode,
        ] = {}

        self.bridge_index: Dict[
            WalletAddress,
            GraphNode,
        ] = {}

        self.program_index: Dict[
            ProgramID,
            GraphNode,
        ] = {}

        self.token_index: Dict[
            TokenMint,
            GraphNode,
        ] = {}

        self.signature_index: Dict[
            Signature,
            List[GraphEdge],
        ] = defaultdict(list)

        self.edge_lookup: Dict[
            Tuple[
                NodeID,
                NodeID,
                EdgeType,
            ],
            GraphEdge,
        ] = {}

        # ==================================================
        # Cache
        # ==================================================

        self.node_cache: Dict[
            NodeID,
            GraphNode,
        ] = {}

        self.edge_cache: Dict[
            str,
            GraphEdge,
        ] = {}

        self.path_cache: Dict[
            Tuple[
                NodeID,
                NodeID,
            ],
            List[NodeID],
        ] = {}

        self.neighbor_cache: Dict[
            NodeID,
            List[NodeID],
        ] = {}

        self.centrality_cache: Dict[
            NodeID,
            float,
        ] = {}

        self.component_cache: Dict[
            int,
            Set[NodeID],
        ] = {}

        self.cache_expiry: Dict[
            str,
            float,
        ] = {}

        # ==================================================
        # Statistics
        # ==================================================

        self.statistics: Dict[
            str,
            Any,
        ] = {

            # Runtime

            "start_time":
                time.time(),

            "last_build":
                None,

            "last_update":
                None,

            # Graph

            "nodes":
                0,

            "edges":
                0,

            "wallet_nodes":
                0,

            "exchange_nodes":
                0,

            "bridge_nodes":
                0,

            "token_nodes":
                0,

            "program_nodes":
                0,

            # Operations

            "graphs_built":
                0,

            "graphs_updated":
                0,

            "transactions_processed":
                0,

            "wallets_processed":
                0,

            "cache_hits":
                0,

            "cache_misses":
                0,

            # Performance

            "build_time":
                0.0,

            "update_time":
                0.0,

            "average_build_time":
                0.0,

            "average_update_time":
                0.0,

        }

        # Performance history

        self._build_history: List[
            float
        ] = []

        self._update_history: List[
            float
        ] = []

        self.logger.info(
            "FundingGraphBuilder initialized."
        )

# ==========================================================
# Part 3
# Graph Building
# ==========================================================

def build_funding_graph(
    self,
    transactions: Optional[
        List[TransactionRecord]
    ] = None,
) -> FundingGraph:
    """
    Build the canonical funding graph.

    Wallet ---> Wallet

    using SOL transfers and token transfers.
    """

    start = time.perf_counter()

    self.graph.status = (
        GraphStatus.BUILDING
    )

    if transactions is None:

        transactions = list(
            self.fetcher.transactions.values()
        )

    # Reset graph

    self.graph.nodes.clear()
    self.graph.edges.clear()
    self.graph.adjacency.clear()
    self.graph.reverse_adjacency.clear()

    self.edge_lookup.clear()
    self.signature_index.clear()

    # ----------------------------------------

    self.build_wallet_graph(
        transactions
    )

    if self.config.build_token_edges:

        self.build_token_graph(
            transactions
        )

    self.graph.updated_at = (
        datetime.utcnow()
    )

    self.graph.status = (
        GraphStatus.READY
    )

    elapsed = (

        time.perf_counter()

        - start

    )

    self.statistics[
        "graphs_built"
    ] += 1

    self.statistics[
        "build_time"
    ] = elapsed

    self._build_history.append(
        elapsed
    )

    self.statistics[
        "average_build_time"
    ] = statistics.mean(
        self._build_history
    )

    self.statistics[
        "last_build"
    ] = datetime.utcnow()

    self.update_statistics()

    return self.graph


# ==========================================================


def build_wallet_graph(
    self,
    transactions: List[
        TransactionRecord
    ],
) -> None:
    """
    Construct wallet-to-wallet
    funding relationships.
    """

    for tx in transactions:

        # ------------------------------
        # Native SOL transfers
        # ------------------------------

        for transfer in tx.sol_transfers:

            sender = transfer.get(
                "from"
            )

            receiver = transfer.get(
                "to"
            )

            if (

                sender is None

                or

                receiver is None

            ):

                continue

            self.add_wallet(
                sender
            )

            self.add_wallet(
                receiver
            )

            self.add_transaction(

                sender,

                receiver,

                tx,

                edge_type=EdgeType.SOL_TRANSFER,

                amount=transfer.get(
                    "sol",
                    0,
                ),

            )

        # ------------------------------
        # SPL transfers
        # ------------------------------

        for transfer in tx.token_transfers:

            sender = transfer.get(
                "from"
            )

            receiver = transfer.get(
                "to"
            )

            if (

                sender is None

                or

                receiver is None

            ):

                continue

            self.add_wallet(
                sender
            )

            self.add_wallet(
                receiver
            )

            self.add_transaction(

                sender,

                receiver,

                tx,

                edge_type=EdgeType.TOKEN_TRANSFER,

                amount=float(

                    transfer.get(
                        "amount",
                        0,
                    )

                ),

                token_mint=transfer.get(
                    "mint"
                ),

            )


# ==========================================================


def build_token_graph(
    self,
    transactions: List[
        TransactionRecord
    ],
) -> None:
    """
    Connect wallets to tokens they
    have interacted with.

    Wallet ---> Token
    """

    for tx in transactions:

        for transfer in tx.token_transfers:

            wallet = transfer.get(
                "to"
            )

            mint = transfer.get(
                "mint"
            )

            if (

                wallet is None

                or

                mint is None

            ):

                continue

            self.add_wallet(
                wallet
            )

            if mint not in self.nodes:

                self.nodes[mint] = GraphNode(

                    id=mint,

                    node_type=NodeType.TOKEN,

                )

            edge = GraphEdge(

                source=wallet,

                target=mint,

                edge_type=EdgeType.TOKEN_TRANSFER,

                signature=tx.signature,

                timestamp=tx.block_time,

                slot=tx.slot,

                token_mint=mint,

                amount=float(

                    transfer.get(
                        "amount",
                        0,
                    )

                ),

            )

            self.graph.edges.append(
                edge
            )

            self.graph.adjacency[
                wallet
            ].add(
                mint
            )

            self.graph.reverse_adjacency[
                mint
            ].add(
                wallet
            )


# ==========================================================


def build_incremental_graph(
    self,
    transactions: List[
        TransactionRecord
    ],
) -> None:
    """
    Incrementally extend the graph.

    Existing nodes remain untouched.

    Only unseen transactions
    are processed.
    """

    processed = 0

    for tx in transactions:

        if (

            tx.signature

            in self.signature_index

        ):

            continue

        self.build_wallet_graph(
            [tx]
        )

        if self.config.build_token_edges:

            self.build_token_graph(
                [tx]
            )

        processed += 1

    self.statistics[
        "graphs_updated"
    ] += 1

    self.statistics[
        "transactions_processed"
    ] += processed

    self.statistics[
        "last_update"
    ] = datetime.utcnow()

    self.graph.updated_at = (
        datetime.utcnow()
    )

    self.update_statistics()

# ==========================================================
# Part 4
# Graph Updates
# ==========================================================

def update_graph(
    self,
    transactions: List[
        TransactionRecord
    ],
) -> FundingGraph:
    """
    Incrementally update the funding graph
    using newly downloaded transactions.

    Existing nodes and edges are preserved.
    """

    start = time.perf_counter()

    self.graph.status = GraphStatus.BUILDING

    self.build_incremental_graph(
        transactions
    )

    self.graph.updated_at = (
        datetime.utcnow()
    )

    self.graph.status = GraphStatus.READY

    elapsed = (
        time.perf_counter()
        - start
    )

    self._update_history.append(
        elapsed
    )

    self.statistics[
        "graphs_updated"
    ] += 1

    self.statistics[
        "update_time"
    ] = elapsed

    self.statistics[
        "average_update_time"
    ] = statistics.mean(
        self._update_history
    )

    self.statistics[
        "last_update"
    ] = datetime.utcnow()

    self.update_statistics()

    return self.graph


# ==========================================================


def update_wallet(
    self,
    wallet: WalletAddress,
) -> None:
    """
    Refresh graph relationships
    for a single wallet.

    Downloads new history and
    updates graph incrementally.
    """

    result = self.fetcher.refresh_history(
        wallet
    )

    if result.transactions:

        self.build_incremental_graph(
            result.transactions
        )

    self.statistics[
        "wallets_processed"
    ] += 1

    self.statistics[
        "last_update"
    ] = datetime.utcnow()


# ==========================================================


def update_transaction(
    self,
    transaction: TransactionRecord,
) -> None:
    """
    Add or replace one transaction
    inside the graph.
    """

    # Remove previous version
    # if already present.

    if (

        transaction.signature

        in self.signature_index

    ):

        self.remove_transaction(
            transaction.signature
        )

    self.build_incremental_graph(
        [transaction]
    )

    self.statistics[
        "transactions_processed"
    ] += 1

    self.statistics[
        "last_update"
    ] = datetime.utcnow()


# ==========================================================


def remove_transaction(
    self,
    signature: Signature,
) -> bool:
    """
    Remove every edge produced
    by a transaction.

    Nodes are intentionally kept
    because they may participate
    in other transactions.
    """

    edges = self.signature_index.get(
        signature
    )

    if not edges:

        return False

    removed = 0

    for edge in list(edges):

        try:

            self.graph.edges.remove(
                edge
            )

        except ValueError:

            continue

        # ----------------------

        self.graph.adjacency[
            edge.source
        ].discard(
            edge.target
        )

        self.graph.reverse_adjacency[
            edge.target
        ].discard(
            edge.source
        )

        key = (

            edge.source,

            edge.target,

            edge.edge_type,

        )

        self.edge_lookup.pop(
            key,
            None,
        )

        removed += 1

    self.signature_index.pop(
        signature,
        None,
    )

    self.statistics[
        "edges"
    ] = max(

        0,

        self.statistics[
            "edges"
        ] - removed,

    )

    self.graph.updated_at = (
        datetime.utcnow()
    )

    self.statistics[
        "last_update"
    ] = datetime.utcnow()

    self.update_statistics()

    return True

# ==========================================================
# Part 5
# Nodes
# ==========================================================

def add_wallet(
    self,
    wallet: WalletAddress,
    *,
    node_type: NodeType = NodeType.WALLET,
    label: Optional[str] = None,
    metadata: Optional[
        JSONDict
    ] = None,
) -> GraphNode:
    """
    Add a wallet (or typed wallet entity)
    to the funding graph.

    If the node already exists, the existing
    node is returned.
    """

    existing = self.wallet_index.get(
        wallet
    )

    if existing is not None:

        return existing

    node = GraphNode(

        id=wallet,

        node_type=node_type,

        label=label,

        metadata=metadata or {},

        first_seen=datetime.utcnow(),

        last_seen=datetime.utcnow(),

    )

    self.graph.nodes[
        wallet
    ] = node

    self.wallet_index[
        wallet
    ] = node

    self.node_cache[
        wallet
    ] = node

    if node_type == NodeType.EXCHANGE:

        self.exchange_index[
            wallet
        ] = node

    elif node_type == NodeType.BRIDGE:

        self.bridge_index[
            wallet
        ] = node

    self.statistics[
        "wallet_nodes"
    ] += 1

    self.statistics[
        "nodes"
    ] = len(
        self.graph.nodes
    )

    return node


# ==========================================================


def remove_wallet(
    self,
    wallet: WalletAddress,
) -> bool:
    """
    Remove a wallet node and all of its
    connected edges.

    This is intended primarily for graph
    maintenance and rebuild operations.
    """

    if wallet not in self.graph.nodes:

        return False

    # ----------------------------------
    # Remove outgoing edges
    # ----------------------------------

    self.graph.edges = [

        edge

        for edge in self.graph.edges

        if (

            edge.source != wallet

            and

            edge.target != wallet

        )

    ]

    # ----------------------------------

    self.graph.adjacency.pop(
        wallet,
        None,
    )

    self.graph.reverse_adjacency.pop(
        wallet,
        None,
    )

    for neighbors in self.graph.adjacency.values():

        neighbors.discard(
            wallet
        )

    for neighbors in self.graph.reverse_adjacency.values():

        neighbors.discard(
            wallet
        )

    self.graph.nodes.pop(
        wallet,
        None,
    )

    self.wallet_index.pop(
        wallet,
        None,
    )

    self.exchange_index.pop(
        wallet,
        None,
    )

    self.bridge_index.pop(
        wallet,
        None,
    )

    self.node_cache.pop(
        wallet,
        None,
    )

    self.statistics[
        "nodes"
    ] = len(
        self.graph.nodes
    )

    self.statistics[
        "wallet_nodes"
    ] = len(
        self.wallet_index
    )

    return True


# ==========================================================


def wallet_exists(
    self,
    wallet: WalletAddress,
) -> bool:
    """
    Determine whether a wallet node
    already exists inside the graph.
    """

    return wallet in self.graph.nodes


# ==========================================================


def wallet_node(
    self,
    wallet: WalletAddress,
) -> Optional[
    GraphNode
]:
    """
    Retrieve a wallet node.

    Cache is checked before the graph.
    """

    cached = self.node_cache.get(
        wallet
    )

    if cached is not None:

        self.statistics[
            "cache_hits"
        ] += 1

        return cached

    self.statistics[
        "cache_misses"
    ] += 1

    node = self.graph.nodes.get(
        wallet
    )

    if node is not None:

        self.node_cache[
            wallet
        ] = node

    return node

# ==========================================================
# Part 6
# Edges
# ==========================================================

def add_transaction(
    self,
    source: NodeID,
    target: NodeID,
    transaction: TransactionRecord,
    *,
    edge_type: EdgeType,
    amount: float = 0.0,
    token_mint: Optional[TokenMint] = None,
    program_id: Optional[ProgramID] = None,
    confidence: float = 1.0,
) -> GraphEdge:
    """
    Create a graph edge from a normalized
    blockchain transaction.

    Duplicate transaction edges are merged by
    increasing weight rather than duplicated.
    """

    return self.add_edge(
        source=source,
        target=target,
        edge_type=edge_type,
        signature=transaction.signature,
        timestamp=transaction.block_time,
        slot=transaction.slot,
        amount=amount,
        token_mint=token_mint,
        program_id=program_id,
        confidence=confidence,
        metadata={
            "fee": transaction.fee,
            "success": transaction.success,
        },
    )


# ==========================================================


def add_edge(
    self,
    *,
    source: NodeID,
    target: NodeID,
    edge_type: EdgeType,
    signature: Optional[Signature] = None,
    timestamp: Optional[int] = None,
    slot: Optional[int] = None,
    amount: float = 0.0,
    token_mint: Optional[TokenMint] = None,
    program_id: Optional[ProgramID] = None,
    confidence: float = 1.0,
    metadata: Optional[JSONDict] = None,
) -> GraphEdge:
    """
    Add an edge to the funding graph.
    """

    key = (
        source,
        target,
        edge_type,
    )

    existing = self.edge_lookup.get(
        key
    )

    if existing is not None:

        existing.weight += 1.0

        existing.amount += amount

        existing.confidence = max(
            existing.confidence,
            confidence,
        )

        if signature:

            self.signature_index[
                signature
            ].append(existing)

        return existing

    edge = GraphEdge(
        source=source,
        target=target,
        edge_type=edge_type,
        signature=signature,
        timestamp=timestamp,
        slot=slot,
        amount=amount,
        token_mint=token_mint,
        program_id=program_id,
        confidence=confidence,
        metadata=metadata or {},
    )

    self.graph.edges.append(edge)

    self.graph.adjacency[
        source
    ].add(target)

    self.graph.reverse_adjacency[
        target
    ].add(source)

    self.edge_lookup[
        key
    ] = edge

    if signature:

        self.signature_index[
            signature
        ].append(edge)

    edge_id = hashlib.sha256(
        (
            f"{source}"
            f"{target}"
            f"{edge_type.value}"
            f"{signature}"
        ).encode()
    ).hexdigest()

    self.edge_cache[
        edge_id
    ] = edge

    self.statistics[
        "edges"
    ] = len(
        self.graph.edges
    )

    return edge


# ==========================================================


def remove_edge(
    self,
    source: NodeID,
    target: NodeID,
    edge_type: EdgeType,
) -> bool:
    """
    Remove a specific edge.
    """

    key = (
        source,
        target,
        edge_type,
    )

    edge = self.edge_lookup.pop(
        key,
        None,
    )

    if edge is None:

        return False

    try:

        self.graph.edges.remove(
            edge
        )

    except ValueError:

        pass

    self.graph.adjacency[
        source
    ].discard(
        target
    )

    self.graph.reverse_adjacency[
        target
    ].discard(
        source
    )

    if edge.signature:

        if edge in self.signature_index.get(
            edge.signature,
            [],
        ):

            self.signature_index[
                edge.signature
            ].remove(edge)

    self.statistics[
        "edges"
    ] = len(
        self.graph.edges
    )

    return True


# ==========================================================


def edge_exists(
    self,
    source: NodeID,
    target: NodeID,
    edge_type: EdgeType,
) -> bool:
    """
    Determine whether an edge exists.
    """

    return (
        source,
        target,
        edge_type,
    ) in self.edge_lookup


# ==========================================================


def edge_weight(
    self,
    source: NodeID,
    target: NodeID,
    edge_type: EdgeType,
) -> float:
    """
    Return the current weight of an edge.

    Weight represents interaction strength
    between two nodes.
    """

    edge = self.edge_lookup.get(
        (
            source,
            target,
            edge_type,
        )
    )

    if edge is None:

        return 0.0

    return edge.weight

# ==========================================================
# Part 7
# Graph Queries
# ==========================================================

from collections import deque

# ==========================================================


def neighbors(
    self,
    node: NodeID,
) -> List[NodeID]:
    """
    Return neighboring nodes directly
    connected to the given node.

    Results are cached.
    """

    cached = self.neighbor_cache.get(
        node
    )

    if cached is not None:

        self.statistics[
            "cache_hits"
        ] += 1

        return cached

    self.statistics[
        "cache_misses"
    ] += 1

    result = list(

        self.graph.adjacency.get(
            node,
            set(),
        )

    )

    self.neighbor_cache[
        node
    ] = result

    return result


# ==========================================================


def incoming_edges(
    self,
    node: NodeID,
) -> List[GraphEdge]:
    """
    Return every edge pointing
    toward a node.
    """

    return [

        edge

        for edge

        in self.graph.edges

        if edge.target == node

    ]


# ==========================================================


def outgoing_edges(
    self,
    node: NodeID,
) -> List[GraphEdge]:
    """
    Return every edge leaving
    a node.
    """

    return [

        edge

        for edge

        in self.graph.edges

        if edge.source == node

    ]


# ==========================================================


def funding_path(
    self,
    source: NodeID,
    destination: NodeID,
) -> Optional[List[NodeID]]:
    """
    Find a funding path using
    breadth-first search.

    Cached for future lookups.
    """

    cache_key = (
        source,
        destination,
    )

    cached = self.path_cache.get(
        cache_key
    )

    if cached is not None:

        self.statistics[
            "cache_hits"
        ] += 1

        return cached

    self.statistics[
        "cache_misses"
    ] += 1

    queue = deque()

    queue.append(
        (
            source,
            [source],
        )
    )

    visited = {
        source
    }

    while queue:

        current, path = (
            queue.popleft()
        )

        if current == destination:

            self.path_cache[
                cache_key
            ] = path

            return path

        for neighbor in self.graph.adjacency.get(
            current,
            set(),
        ):

            if neighbor in visited:

                continue

            visited.add(
                neighbor
            )

            queue.append(

                (
                    neighbor,

                    path + [
                        neighbor
                    ],

                )

            )

    return None


# ==========================================================


def shortest_path(
    self,
    source: NodeID,
    destination: NodeID,
) -> Optional[List[NodeID]]:
    """
    Compute the shortest path between
    two nodes.

    Since the funding graph is currently
    unweighted for routing purposes,
    this is equivalent to BFS.
    """

    return self.funding_path(
        source,
        destination,
    )

# ==========================================================
# Part 8
# Analytics
# ==========================================================

from collections import deque

# ==========================================================


def graph_statistics(
    self,
) -> JSONDict:
    """
    Return high-level statistics describing
    the current funding graph.
    """

    return {

        "status":
            self.graph.status.value,

        "nodes":
            len(self.graph.nodes),

        "edges":
            len(self.graph.edges),

        "wallets":
            len(self.wallet_index),

        "tokens":
            len(self.token_index),

        "programs":
            len(self.program_index),

        "bridges":
            len(self.bridge_index),

        "exchanges":
            len(self.exchange_index),

        "density":
            self.graph_density(),

        "components":
            len(
                self.funding_components()
            ),

        "created_at":
            self.graph.created_at,

        "updated_at":
            self.graph.updated_at,

    }


# ==========================================================


def central_wallets(
    self,
    top_n: int = 25,
) -> List[Tuple[
    WalletAddress,
    int,
]]:
    """
    Rank wallets by total degree
    (incoming + outgoing).
    """

    ranking = []

    for wallet in self.wallet_index:

        degree = (

            len(

                self.graph.adjacency.get(
                    wallet,
                    set(),
                )

            )

            +

            len(

                self.graph.reverse_adjacency.get(
                    wallet,
                    set(),
                )

            )

        )

        ranking.append(
            (
                wallet,
                degree,
            )
        )

    ranking.sort(
        key=lambda item: item[1],
        reverse=True,
    )

    return ranking[:top_n]


# ==========================================================


def isolated_wallets(
    self,
) -> List[
    WalletAddress
]:
    """
    Wallets having zero incoming
    and zero outgoing edges.
    """

    isolated = []

    for wallet in self.wallet_index:

        outgoing = self.graph.adjacency.get(
            wallet,
            set(),
        )

        incoming = self.graph.reverse_adjacency.get(
            wallet,
            set(),
        )

        if (

            len(outgoing) == 0

            and

            len(incoming) == 0

        ):

            isolated.append(
                wallet
            )

    return isolated


# ==========================================================


def funding_components(
    self,
) -> List[
    Set[NodeID]
]:
    """
    Compute connected funding
    components using BFS.

    Components are cached.
    """

    if self.component_cache:

        return list(
            self.component_cache.values()
        )

    visited: Set[
        NodeID
    ] = set()

    components = []

    index = 0

    for node in self.graph.nodes:

        if node in visited:

            continue

        component = set()

        queue = deque(
            [node]
        )

        while queue:

            current = queue.popleft()

            if current in visited:

                continue

            visited.add(
                current
            )

            component.add(
                current
            )

            neighbors = (

                self.graph.adjacency.get(
                    current,
                    set(),
                )

                |

                self.graph.reverse_adjacency.get(
                    current,
                    set(),
                )

            )

            for neighbor in neighbors:

                if neighbor not in visited:

                    queue.append(
                        neighbor
                    )

        self.component_cache[
            index
        ] = component

        components.append(
            component
        )

        index += 1

    return components


# ==========================================================


def graph_density(
    self,
) -> float:
    """
    Compute directed graph density.

    Density =
        E / (N * (N - 1))
    """

    nodes = len(
        self.graph.nodes
    )

    if nodes < 2:

        return 0.0

    maximum_edges = (

        nodes

        *

        (nodes - 1)

    )

    return (

        len(self.graph.edges)

        /

        maximum_edges

    )                                

# ==========================================================
# Part 9
# Persistence
# ==========================================================

import json

# ==========================================================


def save_graph(
    self,
    path: Path | str,
) -> Path:
    """
    Persist the complete funding graph
    as JSON.
    """

    path = Path(path)

    data = self.export_json()

    path.write_text(
        json.dumps(
            data,
            indent=2,
            default=str,
        ),
        encoding="utf-8",
    )

    self.logger.info(
        "Funding graph saved to %s",
        path,
    )

    return path


# ==========================================================


def load_graph(
    self,
    path: Path | str,
) -> FundingGraph:
    """
    Load a funding graph previously
    exported by save_graph().
    """

    path = Path(path)

    data = json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )

    self.graph = FundingGraph()

    self.nodes = self.graph.nodes
    self.edges = self.graph.edges
    self.adjacency = (
        self.graph.adjacency
    )
    self.reverse_adjacency = (
        self.graph.reverse_adjacency
    )

    # -----------------------------
    # Nodes
    # -----------------------------

    for node_data in data["nodes"]:

        node = GraphNode(

            id=node_data["id"],

            node_type=NodeType(
                node_data["node_type"]
            ),

            label=node_data.get(
                "label"
            ),

            metadata=node_data.get(
                "metadata",
                {},
            ),

            risk_score=node_data.get(
                "risk_score",
                0,
            ),

            confidence=node_data.get(
                "confidence",
                1,
            ),

        )

        self.nodes[
            node.id
        ] = node

    # -----------------------------
    # Edges
    # -----------------------------

    for edge_data in data["edges"]:

        edge = GraphEdge(

            source=edge_data["source"],

            target=edge_data["target"],

            edge_type=EdgeType(
                edge_data["edge_type"]
            ),

            signature=edge_data.get(
                "signature"
            ),

            timestamp=edge_data.get(
                "timestamp"
            ),

            slot=edge_data.get(
                "slot"
            ),

            amount=edge_data.get(
                "amount",
                0,
            ),

            token_mint=edge_data.get(
                "token_mint"
            ),

            program_id=edge_data.get(
                "program_id"
            ),

            weight=edge_data.get(
                "weight",
                1,
            ),

            confidence=edge_data.get(
                "confidence",
                1,
            ),

            metadata=edge_data.get(
                "metadata",
                {},
            ),

        )

        self.edges.append(
            edge
        )

        self.adjacency[
            edge.source
        ].add(
            edge.target
        )

        self.reverse_adjacency[
            edge.target
        ].add(
            edge.source
        )

    self.update_statistics()

    self.logger.info(
        "Funding graph loaded."
    )

    return self.graph


# ==========================================================


def export_json(
    self,
) -> JSONDict:
    """
    Export the funding graph as a
    serializable dictionary.
    """

    return {

        "nodes": [

            {

                "id":
                    node.id,

                "node_type":
                    node.node_type.value,

                "label":
                    node.label,

                "metadata":
                    node.metadata,

                "risk_score":
                    node.risk_score,

                "confidence":
                    node.confidence,

            }

            for node

            in self.nodes.values()

        ],

        "edges": [

            {

                "source":
                    edge.source,

                "target":
                    edge.target,

                "edge_type":
                    edge.edge_type.value,

                "signature":
                    edge.signature,

                "timestamp":
                    edge.timestamp,

                "slot":
                    edge.slot,

                "amount":
                    edge.amount,

                "token_mint":
                    edge.token_mint,

                "program_id":
                    edge.program_id,

                "weight":
                    edge.weight,

                "confidence":
                    edge.confidence,

                "metadata":
                    edge.metadata,

            }

            for edge

            in self.edges

        ],

    }


# ==========================================================


def export_graphml(
    self,
    path: Path | str,
) -> Path:
    """
    Export GraphML for Gephi,
    Neo4j import,
    Cytoscape,
    yEd,
    etc.
    """

    import networkx as nx

    graph = self.export_networkx()

    path = Path(path)

    nx.write_graphml(
        graph,
        path,
    )

    return path


# ==========================================================


def export_networkx(
    self,
):
    """
    Convert the funding graph into a
    NetworkX directed graph.

    Useful for graph analytics,
    visualization,
    GraphML,
    GEXF,
    Neo4j pipelines.
    """

    import networkx as nx

    graph = nx.DiGraph()

    # -------------------------

    for node in self.nodes.values():

        graph.add_node(

            node.id,

            node_type=node.node_type.value,

            label=node.label,

            risk=node.risk_score,

            confidence=node.confidence,

            **node.metadata,

        )

    # -------------------------

    for edge in self.edges:

        graph.add_edge(

            edge.source,

            edge.target,

            edge_type=edge.edge_type.value,

            signature=edge.signature,

            amount=edge.amount,

            weight=edge.weight,

            confidence=edge.confidence,

            slot=edge.slot,

            timestamp=edge.timestamp,

            token=edge.token_mint,

            program=edge.program_id,

            **edge.metadata,

        )

    return graph

# ==========================================================
# Part 10
# Cache
# ==========================================================

def refresh_cache(
    self,
) -> None:
    """
    Refresh all runtime caches from the
    current graph state.
    """

    self.node_cache.clear()
    self.edge_cache.clear()
    self.neighbor_cache.clear()
    self.path_cache.clear()
    self.centrality_cache.clear()
    self.component_cache.clear()
    self.cache_expiry.clear()

    # -----------------------------
    # Node cache
    # -----------------------------

    for node in self.nodes.values():

        self.node_cache[
            node.id
        ] = node

    # -----------------------------
    # Edge cache
    # -----------------------------

    for edge in self.edges:

        edge_id = hashlib.sha256(

            (
                f"{edge.source}"
                f"{edge.target}"
                f"{edge.edge_type.value}"
                f"{edge.signature}"
            ).encode()

        ).hexdigest()

        self.edge_cache[
            edge_id
        ] = edge

    # -----------------------------
    # Neighbor cache
    # -----------------------------

    for node in self.nodes:

        self.neighbor_cache[
            node
        ] = list(

            self.graph.adjacency.get(
                node,
                set(),
            )

        )

    now = time.time()

    for key in self.node_cache:

        self.cache_expiry[
            f"node:{key}"
        ] = (
            now
            + self.config.cache_ttl
        )

    self.logger.info(
        "Graph cache refreshed."
    )


# ==========================================================


def clear_cache(
    self,
) -> None:
    """
    Completely clear every runtime cache.
    """

    self.node_cache.clear()

    self.edge_cache.clear()

    self.path_cache.clear()

    self.neighbor_cache.clear()

    self.centrality_cache.clear()

    self.component_cache.clear()

    self.cache_expiry.clear()

    self.logger.info(
        "Graph cache cleared."
    )


# ==========================================================


def rebuild_indexes(
    self,
) -> None:
    """
    Rebuild every lookup index from the
    current graph.
    """

    self.wallet_index.clear()

    self.exchange_index.clear()

    self.bridge_index.clear()

    self.token_index.clear()

    self.program_index.clear()

    self.signature_index.clear()

    self.edge_lookup.clear()

    # -----------------------------
    # Nodes
    # -----------------------------

    for node in self.nodes.values():

        if node.node_type == NodeType.WALLET:

            self.wallet_index[
                node.id
            ] = node

        elif node.node_type == NodeType.EXCHANGE:

            self.exchange_index[
                node.id
            ] = node

        elif node.node_type == NodeType.BRIDGE:

            self.bridge_index[
                node.id
            ] = node

        elif node.node_type == NodeType.TOKEN:

            self.token_index[
                node.id
            ] = node

        elif node.node_type == NodeType.PROGRAM:

            self.program_index[
                node.id
            ] = node

    # -----------------------------
    # Edges
    # -----------------------------

    for edge in self.edges:

        key = (

            edge.source,

            edge.target,

            edge.edge_type,

        )

        self.edge_lookup[
            key
        ] = edge

        if edge.signature:

            self.signature_index[
                edge.signature
            ].append(edge)

    self.logger.info(
        "Graph indexes rebuilt."
    )


# ==========================================================


def update_statistics(
    self,
) -> Dict[str, Any]:
    """
    Refresh graph statistics.
    """

    self.statistics[
        "nodes"
    ] = len(
        self.nodes
    )

    self.statistics[
        "edges"
    ] = len(
        self.edges
    )

    self.statistics[
        "wallet_nodes"
    ] = len(
        self.wallet_index
    )

    self.statistics[
        "exchange_nodes"
    ] = len(
        self.exchange_index
    )

    self.statistics[
        "bridge_nodes"
    ] = len(
        self.bridge_index
    )

    self.statistics[
        "token_nodes"
    ] = len(
        self.token_index
    )

    self.statistics[
        "program_nodes"
    ] = len(
        self.program_index
    )

    self.statistics[
        "cache_size"
    ] = (

        len(self.node_cache)

        +

        len(self.edge_cache)

        +

        len(self.path_cache)

        +

        len(self.neighbor_cache)

    )

    self.statistics[
        "uptime_seconds"
    ] = (

        time.time()

        -

        self.statistics[
            "start_time"
        ]

    )

    self.statistics[
        "graph_density"
    ] = self.graph_density()

    self.statistics[
        "connected_components"
    ] = len(
        self.funding_components()
    )

    return self.statistics

# ==========================================================
# Part 11
# Engine
# ==========================================================

def build(
    self,
    transactions: Optional[
        List[TransactionRecord]
    ] = None,
) -> FundingGraph:
    """
    Primary entry point for building the
    funding graph.

    This method is typically called during
    application startup or the initial
    blockchain synchronization.
    """

    self.logger.info(
        "Building funding graph..."
    )

    graph = self.build_funding_graph(
        transactions
    )

    self.refresh_cache()

    self.rebuild_indexes()

    self.update_statistics()

    if self.config.save_on_build:

        try:

            self.save_graph(
                "funding_graph.json"
            )

        except Exception as exc:

            self.logger.warning(
                "Unable to save graph: %s",
                exc,
            )

    return graph


# ==========================================================


def rebuild(
    self,
) -> FundingGraph:
    """
    Completely rebuild the funding graph
    from every cached transaction.

    Existing graph structures are discarded.
    """

    self.logger.info(
        "Performing full graph rebuild..."
    )

    self.clear_cache()

    self.graph = FundingGraph()

    self.nodes = self.graph.nodes
    self.edges = self.graph.edges
    self.adjacency = (
        self.graph.adjacency
    )
    self.reverse_adjacency = (
        self.graph.reverse_adjacency
    )

    self.rebuild_indexes()

    graph = self.build_funding_graph()

    self.refresh_cache()

    self.update_statistics()

    return graph


# ==========================================================


def synchronize(
    self,
) -> FundingGraph:
    """
    Synchronize the funding graph with the
    latest blockchain state.

    New transactions are fetched from the
    TransactionFetcher and applied
    incrementally whenever possible.
    """

    self.logger.info(
        "Synchronizing funding graph..."
    )

    transactions = list(
        self.fetcher.transactions.values()
    )

    self.update_graph(
        transactions
    )

    self.refresh_cache()

    self.rebuild_indexes()

    self.update_statistics()

    return self.graph


# ==========================================================


def shutdown(
    self,
    *,
    save: bool = True,
    path: str = "funding_graph.json",
) -> None:
    """
    Gracefully shut down the graph engine.

    Saves the graph if configured and
    releases runtime resources.
    """

    self.logger.info(
        "Shutting down FundingGraphBuilder..."
    )

    if save:

        try:

            self.save_graph(path)

        except Exception as exc:

            self.logger.warning(
                "Failed to save graph during shutdown: %s",
                exc,
            )

    self.clear_cache()

    self.statistics[
        "shutdown_time"
    ] = datetime.utcnow()

    self.logger.info(
        "FundingGraphBuilder stopped successfully."
    )        