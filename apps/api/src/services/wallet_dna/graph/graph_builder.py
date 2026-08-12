"""
Sentinel AI
Wallet DNA Graph Builder

Part 1A
- Imports
- Constants
- Enums
- Type Aliases
"""

from __future__ import annotations

from enum import Enum
from typing import (
    Dict,
    List,
    Set,
    Tuple,
    Optional,
    Any,
    Union,
    Iterable,
    TypeAlias,
)

from datetime import datetime
from uuid import uuid4

import networkx as nx

# ==========================================================
# Graph Configuration
# ==========================================================

GRAPH_VERSION = "1.0.0"

DEFAULT_GRAPH_NAME = "Sentinel Wallet DNA"

MAX_GRAPH_DEPTH = 10

MAX_NODE_COUNT = 100_000

MAX_EDGE_COUNT = 500_000

DEFAULT_EDGE_WEIGHT = 1.0

DEFAULT_CONFIDENCE = 1.0

DEFAULT_RISK_SCORE = 0.0

DEFAULT_SIMILARITY_SCORE = 0.0

# ==========================================================
# Node Types
# ==========================================================


class NodeType(str, Enum):
    WALLET = "wallet"

    TOKEN = "token"

    DEPLOYER = "deployer"

    EXCHANGE = "exchange"

    CONTRACT = "contract"

    POOL = "pool"

    BRIDGE = "bridge"

    UNKNOWN = "unknown"


# ==========================================================
# Edge Types
# ==========================================================


class EdgeType(str, Enum):
    TRANSFER = "transfer"

    FUNDING = "funding"

    DEPLOYED = "deployed"

    HOLDS = "holds"

    SOLD = "sold"

    BOUGHT = "bought"

    SWAPPED = "swapped"

    LIQUIDITY = "liquidity"

    INTERACTED = "interacted"

    BUNDLE = "bundle"

    JITO = "jito"

    MEV = "mev"

    RELATED = "related"

    SIMILAR = "similar"

    UNKNOWN = "unknown"


# ==========================================================
# Wallet Labels
# ==========================================================


class WalletLabel(str, Enum):
    NORMAL = "normal"

    WHALE = "whale"

    SMART_MONEY = "smart_money"

    SNIPER = "sniper"

    DEPLOYER = "deployer"

    INSIDER = "insider"

    EXCHANGE = "exchange"

    MARKET_MAKER = "market_maker"

    BOT = "bot"

    JITO_SEARCHER = "jito_searcher"

    MEV_SEARCHER = "mev_searcher"

    TEAM = "team"

    UNKNOWN = "unknown"


# ==========================================================
# Graph Status
# ==========================================================


class GraphStatus(str, Enum):
    INITIALIZING = "initializing"

    BUILDING = "building"

    READY = "ready"

    FAILED = "failed"

    UPDATING = "updating"


# ==========================================================
# Risk Levels
# ==========================================================


class RiskLevel(str, Enum):
    SAFE = "safe"

    LOW = "low"

    MEDIUM = "medium"

    HIGH = "high"

    CRITICAL = "critical"


# ==========================================================
# Type Aliases
# ==========================================================

WalletAddress: TypeAlias = str

TokenAddress: TypeAlias = str

NodeId: TypeAlias = str

EdgeId: TypeAlias = str

Timestamp: TypeAlias = datetime

GraphObject: TypeAlias = nx.MultiDiGraph

Attributes: TypeAlias = Dict[str, Any]

NodeCollection: TypeAlias = Dict[NodeId, Any]

EdgeCollection: TypeAlias = Dict[EdgeId, Any]

NeighborSet: TypeAlias = Set[NodeId]

Path: TypeAlias = List[NodeId]

Weight = float

Confidence = float

RiskScore = float

SimilarityScore = float

# ==========================================================
# Helpers
# ==========================================================


def generate_node_id() -> NodeId:
    return str(uuid4())


def generate_edge_id() -> EdgeId:
    return str(uuid4())


def now() -> Timestamp:
    return datetime.utcnow()

# ==========================================================
# Part 1B
# Wallet DNA Graph Models
# ==========================================================

from dataclasses import dataclass, field


# ==========================================================
# Wallet Node
# ==========================================================

@dataclass
class WalletNode:
    """
    Represents a node inside the Wallet DNA graph.
    """

    id: NodeId

    address: WalletAddress

    node_type: NodeType = NodeType.WALLET

    label: WalletLabel = WalletLabel.NORMAL

    name: Optional[str] = None

    tags: List[str] = field(default_factory=list)

    risk_level: RiskLevel = RiskLevel.LOW

    risk_score: RiskScore = DEFAULT_RISK_SCORE

    similarity_score: SimilarityScore = DEFAULT_SIMILARITY_SCORE

    confidence: Confidence = DEFAULT_CONFIDENCE

    balance_sol: float = 0.0

    usd_value: float = 0.0

    tx_count: int = 0

    token_count: int = 0

    first_seen: Timestamp = field(default_factory=now)

    last_seen: Timestamp = field(default_factory=now)

    metadata: Attributes = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "address": self.address,
            "node_type": self.node_type.value,
            "label": self.label.value,
            "name": self.name,
            "tags": self.tags,
            "risk_level": self.risk_level.value,
            "risk_score": self.risk_score,
            "similarity_score": self.similarity_score,
            "confidence": self.confidence,
            "balance_sol": self.balance_sol,
            "usd_value": self.usd_value,
            "tx_count": self.tx_count,
            "token_count": self.token_count,
            "first_seen": self.first_seen.isoformat(),
            "last_seen": self.last_seen.isoformat(),
            "metadata": self.metadata,
        }


# ==========================================================
# Graph Edge
# ==========================================================

@dataclass
class GraphEdge:
    """
    Connection between two Wallet DNA nodes.
    """

    id: EdgeId

    source: NodeId

    target: NodeId

    edge_type: EdgeType

    weight: Weight = DEFAULT_EDGE_WEIGHT

    confidence: Confidence = DEFAULT_CONFIDENCE

    amount_sol: float = 0.0

    amount_usd: float = 0.0

    token: Optional[str] = None

    tx_signature: Optional[str] = None

    block_time: Timestamp = field(default_factory=now)

    metadata: Attributes = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "source": self.source,
            "target": self.target,
            "edge_type": self.edge_type.value,
            "weight": self.weight,
            "confidence": self.confidence,
            "amount_sol": self.amount_sol,
            "amount_usd": self.amount_usd,
            "token": self.token,
            "tx_signature": self.tx_signature,
            "block_time": self.block_time.isoformat(),
            "metadata": self.metadata,
        }


# ==========================================================
# Graph Metadata
# ==========================================================

@dataclass
class GraphMetadata:
    """
    Metadata describing the current graph.
    """

    graph_name: str = DEFAULT_GRAPH_NAME

    version: str = GRAPH_VERSION

    status: GraphStatus = GraphStatus.INITIALIZING

    created_at: Timestamp = field(default_factory=now)

    updated_at: Timestamp = field(default_factory=now)

    node_count: int = 0

    edge_count: int = 0

    wallet_count: int = 0

    deployer_count: int = 0

    token_count: int = 0

    exchange_count: int = 0

    description: str = ""

    metadata: Attributes = field(default_factory=dict)

    def touch(self):
        self.updated_at = now()

    def to_dict(self) -> dict:
        return {
            "graph_name": self.graph_name,
            "version": self.version,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "node_count": self.node_count,
            "edge_count": self.edge_count,
            "wallet_count": self.wallet_count,
            "deployer_count": self.deployer_count,
            "token_count": self.token_count,
            "exchange_count": self.exchange_count,
            "description": self.description,
            "metadata": self.metadata,
        }    

# ==========================================================
# Part 1C
# GraphBuilder Core
# ==========================================================


class GraphBuilder:
    """
    Core Wallet DNA graph engine.

    This class owns the NetworkX graph and provides the
    foundation for:

    - Funding graphs
    - Wallet relationship graphs
    - Whale clusters
    - Smart Money clusters
    - Deployer graphs
    - Capital flow graphs
    """

    def __init__(
        self,
        name: str = DEFAULT_GRAPH_NAME,
    ) -> None:

        # --------------------------------------------------
        # Graph Metadata
        # --------------------------------------------------

        self.metadata = GraphMetadata(
            graph_name=name,
            status=GraphStatus.INITIALIZING,
        )

        # --------------------------------------------------
        # NetworkX Graph
        # --------------------------------------------------

        # Directed multigraph:
        # Wallet A ----> Wallet B
        # Multiple transaction edges are allowed.
        self.graph: GraphObject = nx.MultiDiGraph(
            name=name,
        )

        # --------------------------------------------------
        # Internal Storage
        # --------------------------------------------------

        self.nodes: NodeCollection = {}

        self.edges: EdgeCollection = {}

        # Quick lookup
        self.address_to_node: Dict[
            WalletAddress,
            NodeId,
        ] = {}

        # Node -> Connected Edges
        self.node_edges: Dict[
            NodeId,
            Set[EdgeId],
        ] = {}

        # Labels
        self.wallet_labels: Dict[
            WalletAddress,
            WalletLabel,
        ] = {}

        # Graph statistics cache
        self.stats: Dict[str, Any] = {
            "wallets": 0,
            "tokens": 0,
            "deployers": 0,
            "contracts": 0,
            "exchanges": 0,
            "bridges": 0,
            "edges": 0,
        }

        # Internal caches
        self._degree_cache: Dict[
            NodeId,
            int,
        ] = {}

        self._centrality_cache: Dict[
            NodeId,
            float,
        ] = {}

        self._path_cache: Dict[
            tuple,
            List[NodeId],
        ] = {}

        self.metadata.status = GraphStatus.READY

    # =====================================================
    # Basic Properties
    # =====================================================

    @property
    def node_count(self) -> int:
        return len(self.nodes)

    @property
    def edge_count(self) -> int:
        return len(self.edges)

    @property
    def graph_name(self) -> str:
        return self.metadata.graph_name

    # =====================================================
    # Graph State
    # =====================================================

    def clear(self) -> None:
        """
        Reset graph.
        """

        self.graph.clear()

        self.nodes.clear()

        self.edges.clear()

        self.address_to_node.clear()

        self.node_edges.clear()

        self.wallet_labels.clear()

        self._degree_cache.clear()

        self._centrality_cache.clear()

        self._path_cache.clear()

        self.stats = {
            "wallets": 0,
            "tokens": 0,
            "deployers": 0,
            "contracts": 0,
            "exchanges": 0,
            "bridges": 0,
            "edges": 0,
        }

        self.metadata.node_count = 0
        self.metadata.edge_count = 0
        self.metadata.wallet_count = 0
        self.metadata.token_count = 0
        self.metadata.deployer_count = 0
        self.metadata.exchange_count = 0

        self.metadata.touch()

    # =====================================================
    # Metadata
    # =====================================================

    def update_metadata(self) -> None:
        """
        Refresh metadata counters.
        """

        self.metadata.node_count = self.node_count

        self.metadata.edge_count = self.edge_count

        self.metadata.wallet_count = self.stats["wallets"]

        self.metadata.token_count = self.stats["tokens"]

        self.metadata.deployer_count = self.stats["deployers"]

        self.metadata.exchange_count = self.stats["exchanges"]

        self.metadata.touch()

    # =====================================================
    # Graph Summary
    # =====================================================

    def summary(self) -> dict:
        """
        Returns a quick overview of the graph.
        """

        self.update_metadata()

        return {
            "metadata": self.metadata.to_dict(),
            "nodes": self.node_count,
            "edges": self.edge_count,
            "stats": self.stats,
        }

    # =====================================================
    # Helpers
    # =====================================================

    def has_node(
        self,
        node_id: NodeId,
    ) -> bool:
        return node_id in self.nodes

    def has_address(
        self,
        address: WalletAddress,
    ) -> bool:
        return address in self.address_to_node

    def has_edge(
        self,
        edge_id: EdgeId,
    ) -> bool:
        return edge_id in self.edges        

# =====================================================
# Validation Helpers
# =====================================================

def _validate_node(self, node: WalletNode) -> None:
    """
    Validate a WalletNode before inserting into the graph.
    """

    if not isinstance(node, WalletNode):
        raise TypeError("node must be an instance of WalletNode")

    if not node.id:
        raise ValueError("Node ID cannot be empty.")

    if not node.address:
        raise ValueError("Wallet address cannot be empty.")

    if not isinstance(node.node_type, NodeType):
        raise TypeError("Invalid NodeType.")

    if not isinstance(node.label, WalletLabel):
        raise TypeError("Invalid WalletLabel.")

    if not isinstance(node.risk_level, RiskLevel):
        raise TypeError("Invalid RiskLevel.")

    if node.confidence < 0 or node.confidence > 1:
        raise ValueError("Confidence must be between 0 and 1.")

    if node.similarity_score < 0 or node.similarity_score > 1:
        raise ValueError("Similarity score must be between 0 and 1.")

    if node.risk_score < 0 or node.risk_score > 100:
        raise ValueError("Risk score must be between 0 and 100.")

    if node.balance_sol < 0:
        raise ValueError("Balance cannot be negative.")

    if node.tx_count < 0:
        raise ValueError("Transaction count cannot be negative.")

    if node.token_count < 0:
        raise ValueError("Token count cannot be negative.")


def _validate_node_id(self, node_id: NodeId) -> None:
    """
    Validate node ID.
    """

    if not node_id:
        raise ValueError("Node ID cannot be empty.")

    if not isinstance(node_id, str):
        raise TypeError("Node ID must be a string.")


def _validate_wallet_address(self, address: WalletAddress) -> None:
    """
    Validate wallet address.
    """

    if not address:
        raise ValueError("Wallet address cannot be empty.")

    if not isinstance(address, str):
        raise TypeError("Wallet address must be a string.")

    if len(address.strip()) < 32:
        raise ValueError("Wallet address appears to be invalid.")


def _node_exists(self, node_id: NodeId) -> bool:
    """
    Returns True if node exists.
    """

    return node_id in self.nodes


def _address_exists(self, address: WalletAddress) -> bool:
    """
    Returns True if wallet already exists.
    """

    return address in self.address_to_node


def _ensure_node_not_exists(self, node: WalletNode) -> None:
    """
    Prevent duplicate node IDs or addresses.
    """

    if self._node_exists(node.id):
        raise ValueError(
            f"Node '{node.id}' already exists."
        )

    if self._address_exists(node.address):
        raise ValueError(
            f"Wallet '{node.address}' already exists."
        )


def _register_node(self, node: WalletNode) -> None:
    """
    Register internal indexes.
    """

    self.nodes[node.id] = node

    self.address_to_node[node.address] = node.id

    self.node_edges.setdefault(node.id, set())


def _update_node_statistics(self, node: WalletNode) -> None:
    """
    Update graph statistics.
    """

    self.metadata.node_count += 1

    if node.node_type == NodeType.WALLET:
        self.stats["wallets"] += 1
        self.metadata.wallet_count += 1

    elif node.node_type == NodeType.TOKEN:
        self.stats["tokens"] += 1
        self.metadata.token_count += 1

    elif node.node_type == NodeType.DEPLOYER:
        self.stats["deployers"] += 1
        self.metadata.deployer_count += 1

    elif node.node_type == NodeType.EXCHANGE:
        self.stats["exchanges"] += 1
        self.metadata.exchange_count += 1

    elif node.node_type == NodeType.CONTRACT:
        self.stats["contracts"] += 1

    elif node.node_type == NodeType.BRIDGE:
        self.stats["bridges"] += 1

    self.metadata.touch()

# =====================================================
# Node Operations
# add_node()
# =====================================================

def add_node(self, node: WalletNode) -> WalletNode:
    """
    Add a WalletNode to the Wallet DNA graph.

    This method:
        • Validates the node
        • Prevents duplicates
        • Registers internal indexes
        • Adds the node to the NetworkX graph
        • Updates statistics
        • Returns the inserted node
    """

    # -----------------------------
    # Validate
    # -----------------------------
    self._validate_node(node)

    self._ensure_node_not_exists(node)

    # -----------------------------
    # Register internal collections
    # -----------------------------
    self._register_node(node)

    # -----------------------------
    # Add into NetworkX graph
    # -----------------------------
    self.graph.add_node(
        node.id,

        address=node.address,

        node_type=node.node_type.value,

        label=node.label.value,

        name=node.name,

        tags=list(node.tags),

        risk_level=node.risk_level.value,

        risk_score=node.risk_score,

        similarity_score=node.similarity_score,

        confidence=node.confidence,

        balance_sol=node.balance_sol,

        usd_value=node.usd_value,

        tx_count=node.tx_count,

        token_count=node.token_count,

        first_seen=node.first_seen,

        last_seen=node.last_seen,

        metadata=dict(node.metadata),
    )

    # -----------------------------
    # Update statistics
    # -----------------------------
    self._update_node_statistics(node)

    # -----------------------------
    # Refresh graph metadata
    # -----------------------------
    self.update_metadata()

    return node


# =====================================================
# Convenience Methods
# =====================================================

def add_wallet(
    self,
    address: WalletAddress,
    **kwargs,
) -> WalletNode:
    """
    Create and insert a wallet node.
    """

    node = WalletNode(
        id=generate_node_id(),
        address=address,
        node_type=NodeType.WALLET,
        **kwargs,
    )

    return self.add_node(node)


def add_token(
    self,
    address: WalletAddress,
    **kwargs,
) -> WalletNode:
    """
    Create and insert a token node.
    """

    node = WalletNode(
        id=generate_node_id(),
        address=address,
        node_type=NodeType.TOKEN,
        **kwargs,
    )

    return self.add_node(node)


def add_deployer(
    self,
    address: WalletAddress,
    **kwargs,
) -> WalletNode:
    """
    Create and insert a deployer node.
    """

    node = WalletNode(
        id=generate_node_id(),
        address=address,
        node_type=NodeType.DEPLOYER,
        label=WalletLabel.DEPLOYER,
        **kwargs,
    )

    return self.add_node(node)


def add_exchange(
    self,
    address: WalletAddress,
    **kwargs,
) -> WalletNode:
    """
    Create and insert an exchange node.
    """

    node = WalletNode(
        id=generate_node_id(),
        address=address,
        node_type=NodeType.EXCHANGE,
        label=WalletLabel.EXCHANGE,
        **kwargs,
    )

    return self.add_node(node)


def add_contract(
    self,
    address: WalletAddress,
    **kwargs,
) -> WalletNode:
    """
    Create and insert a contract node.
    """

    node = WalletNode(
        id=generate_node_id(),
        address=address,
        node_type=NodeType.CONTRACT,
        **kwargs,
    )

    return self.add_node(node)

# =====================================================
# Node Retrieval Operations
# =====================================================

def get_node(
    self,
    node_id: NodeId,
) -> Optional[WalletNode]:
    """
    Retrieve a node by its unique Node ID.

    Returns
    -------
    WalletNode | None
    """

    self._validate_node_id(node_id)

    return self.nodes.get(node_id)


def get_node_or_raise(
    self,
    node_id: NodeId,
) -> WalletNode:
    """
    Retrieve a node or raise KeyError if it doesn't exist.
    """

    node = self.get_node(node_id)

    if node is None:
        raise KeyError(
            f"Node '{node_id}' does not exist."
        )

    return node


def get_node_by_address(
    self,
    address: WalletAddress,
) -> Optional[WalletNode]:
    """
    Retrieve a node using its wallet address.

    Returns
    -------
    WalletNode | None
    """

    self._validate_wallet_address(address)

    node_id = self.address_to_node.get(address)

    if node_id is None:
        return None

    return self.nodes.get(node_id)


def get_node_by_address_or_raise(
    self,
    address: WalletAddress,
) -> WalletNode:
    """
    Retrieve a node by wallet address or raise KeyError.
    """

    node = self.get_node_by_address(address)

    if node is None:
        raise KeyError(
            f"Wallet '{address}' does not exist."
        )

    return node


def has_node_id(
    self,
    node_id: NodeId,
) -> bool:
    """
    Check whether a Node ID exists.
    """

    self._validate_node_id(node_id)

    return node_id in self.nodes


def has_wallet(
    self,
    address: WalletAddress,
) -> bool:
    """
    Check whether a wallet address exists.
    """

    self._validate_wallet_address(address)

    return address in self.address_to_node


def get_node_id(
    self,
    address: WalletAddress,
) -> Optional[NodeId]:
    """
    Get the Node ID associated with a wallet address.
    """

    self._validate_wallet_address(address)

    return self.address_to_node.get(address)

# =====================================================
# Edge Operations
# =====================================================

def _validate_edge(
    self,
    edge: GraphEdge,
) -> None:
    """
    Validate GraphEdge.
    """

    if not isinstance(edge, GraphEdge):
        raise TypeError("edge must be GraphEdge")

    if not edge.id:
        raise ValueError("Edge ID cannot be empty.")

    if edge.source == edge.target:
        raise ValueError("Self-loop edges are not allowed.")

    if edge.source not in self.nodes:
        raise KeyError(f"Source node '{edge.source}' does not exist.")

    if edge.target not in self.nodes:
        raise KeyError(f"Target node '{edge.target}' does not exist.")

    if not isinstance(edge.edge_type, EdgeType):
        raise TypeError("Invalid EdgeType.")

    if edge.weight < 0:
        raise ValueError("Weight cannot be negative.")

    if edge.confidence < 0 or edge.confidence > 1:
        raise ValueError("Confidence must be between 0 and 1.")


def add_edge(
    self,
    edge: GraphEdge,
) -> GraphEdge:
    """
    Add a relationship edge.
    """

    self._validate_edge(edge)

    if edge.id in self.edges:
        raise ValueError(
            f"Edge '{edge.id}' already exists."
        )

    self.edges[edge.id] = edge

    self.node_edges.setdefault(
        edge.source,
        set(),
    ).add(edge.id)

    self.node_edges.setdefault(
        edge.target,
        set(),
    ).add(edge.id)

    self.graph.add_edge(
        edge.source,
        edge.target,
        key=edge.id,

        edge_type=edge.edge_type.value,

        weight=edge.weight,

        confidence=edge.confidence,

        amount_sol=edge.amount_sol,

        amount_usd=edge.amount_usd,

        token=edge.token,

        tx_signature=edge.tx_signature,

        block_time=edge.block_time,

        metadata=edge.metadata,
    )

    self.stats["edges"] += 1

    self.metadata.edge_count += 1

    self.metadata.touch()

    return edge


# =====================================================
# Convenience Edge Builders
# =====================================================

def connect(
    self,
    source: NodeId,
    target: NodeId,
    edge_type: EdgeType,
    **kwargs,
) -> GraphEdge:
    """
    Quickly connect two nodes.
    """

    edge = GraphEdge(
        id=generate_edge_id(),

        source=source,

        target=target,

        edge_type=edge_type,

        **kwargs,
    )

    return self.add_edge(edge)


def add_transfer(
    self,
    source: NodeId,
    target: NodeId,
    amount_sol: float,
    **kwargs,
) -> GraphEdge:
    """
    SOL transfer edge.
    """

    return self.connect(
        source,
        target,
        EdgeType.TRANSFER,
        amount_sol=amount_sol,
        **kwargs,
    )


def add_funding(
    self,
    source: NodeId,
    target: NodeId,
    amount_sol: float,
    **kwargs,
) -> GraphEdge:
    """
    Funding relationship.
    """

    return self.connect(
        source,
        target,
        EdgeType.FUNDING,
        amount_sol=amount_sol,
        **kwargs,
    )


def add_swap(
    self,
    source: NodeId,
    target: NodeId,
    token: str,
    amount_usd: float,
    **kwargs,
) -> GraphEdge:
    """
    Swap relationship.
    """

    return self.connect(
        source,
        target,
        EdgeType.SWAPPED,
        token=token,
        amount_usd=amount_usd,
        **kwargs,
    )


def add_related_wallet(
    self,
    source: NodeId,
    target: NodeId,
    confidence: float = 1.0,
    **kwargs,
) -> GraphEdge:
    """
    Wallet similarity edge.
    """

    return self.connect(
        source,
        target,
        EdgeType.RELATED,
        confidence=confidence,
        **kwargs,
    )            

# =====================================================
# Edge Lookup Operations
# =====================================================

def edge_exists(
    self,
    edge_id: EdgeId,
) -> bool:
    """
    Check whether an edge exists.

    Parameters
    ----------
    edge_id : EdgeId

    Returns
    -------
    bool
    """

    if not edge_id:
        return False

    return edge_id in self.edges


def get_edge(
    self,
    edge_id: EdgeId,
) -> Optional[GraphEdge]:
    """
    Retrieve a GraphEdge by its ID.

    Parameters
    ----------
    edge_id : EdgeId

    Returns
    -------
    GraphEdge | None
    """

    if not edge_id:
        return None

    return self.edges.get(edge_id)


def get_edge_or_raise(
    self,
    edge_id: EdgeId,
) -> GraphEdge:
    """
    Retrieve an edge or raise KeyError.
    """

    edge = self.get_edge(edge_id)

    if edge is None:
        raise KeyError(
            f"Edge '{edge_id}' does not exist."
        )

    return edge


def get_edges(
    self,
) -> List[GraphEdge]:
    """
    Return every edge in the graph.
    """

    return list(self.edges.values())


def get_edge_count(
    self,
) -> int:
    """
    Return total edge count.
    """

    return len(self.edges)


def iter_edges(
    self,
):
    """
    Iterate over every edge.
    """

    yield from self.edges.values()


def get_edges_by_type(
    self,
    edge_type: EdgeType,
) -> List[GraphEdge]:
    """
    Return every edge of a given type.
    """

    if not isinstance(edge_type, EdgeType):
        raise TypeError(
            "edge_type must be EdgeType."
        )

    return [
        edge
        for edge in self.edges.values()
        if edge.edge_type == edge_type
    ]


def get_edges_by_token(
    self,
    token: str,
) -> List[GraphEdge]:
    """
    Return all edges involving a token.
    """

    if not token:
        return []

    return [
        edge
        for edge in self.edges.values()
        if edge.token == token
    ]


def get_transaction_edge(
    self,
    signature: str,
) -> Optional[GraphEdge]:
    """
    Find an edge by transaction signature.
    """

    if not signature:
        return None

    for edge in self.edges.values():

        if edge.tx_signature == signature:

            return edge

    return None

# =====================================================
# Graph Traversal Operations
# =====================================================

def get_edges_between(
    self,
    source: NodeId,
    target: NodeId,
) -> List[GraphEdge]:
    """
    Return every edge connecting source -> target.
    """

    self._validate_node_id(source)
    self._validate_node_id(target)

    if source not in self.nodes:
        raise KeyError(f"Unknown source node '{source}'.")

    if target not in self.nodes:
        raise KeyError(f"Unknown target node '{target}'.")

    result: List[GraphEdge] = []

    for edge in self.edges.values():

        if edge.source == source and edge.target == target:

            result.append(edge)

    return result


def incoming_edges(
    self,
    node_id: NodeId,
) -> List[GraphEdge]:
    """
    Return every incoming edge.
    """

    self._validate_node_id(node_id)

    if node_id not in self.nodes:
        raise KeyError(f"Unknown node '{node_id}'.")

    return [
        edge
        for edge in self.edges.values()
        if edge.target == node_id
    ]


def outgoing_edges(
    self,
    node_id: NodeId,
) -> List[GraphEdge]:
    """
    Return every outgoing edge.
    """

    self._validate_node_id(node_id)

    if node_id not in self.nodes:
        raise KeyError(f"Unknown node '{node_id}'.")

    return [
        edge
        for edge in self.edges.values()
        if edge.source == node_id
    ]


def edge_degree(
    self,
    node_id: NodeId,
) -> int:
    """
    Total edge degree.
    """

    return len(self.incoming_edges(node_id)) + len(
        self.outgoing_edges(node_id)
    )


def in_degree(
    self,
    node_id: NodeId,
) -> int:
    """
    Incoming edge count.
    """

    return len(self.incoming_edges(node_id))


def out_degree(
    self,
    node_id: NodeId,
) -> int:
    """
    Outgoing edge count.
    """

    return len(self.outgoing_edges(node_id))


def has_connection(
    self,
    source: NodeId,
    target: NodeId,
) -> bool:
    """
    Returns True if any edge exists between
    source and target.
    """

    return len(
        self.get_edges_between(
            source,
            target,
        )
    ) > 0


def first_edge_between(
    self,
    source: NodeId,
    target: NodeId,
) -> Optional[GraphEdge]:
    """
    Returns first edge between two nodes.
    """

    edges = self.get_edges_between(
        source,
        target,
    )

    if not edges:
        return None

    return edges[0]

# =====================================================
# Edge Update / Removal Operations
# =====================================================

def update_edge(
    self,
    edge_id: EdgeId,
    **updates,
) -> GraphEdge:
    """
    Update an existing edge.
    """

    edge = self.get_edge_or_raise(edge_id)

    immutable = {
        "id",
        "source",
        "target",
    }

    for key, value in updates.items():

        if key in immutable:
            continue

        if hasattr(edge, key):
            setattr(edge, key, value)

    self._validate_edge(edge)

    if self.graph.has_edge(
        edge.source,
        edge.target,
        key=edge.id,
    ):

        attrs = self.graph[
            edge.source
        ][
            edge.target
        ][
            edge.id
        ]

        attrs.update(
            {
                "edge_type": edge.edge_type.value,
                "weight": edge.weight,
                "confidence": edge.confidence,
                "amount_sol": edge.amount_sol,
                "amount_usd": edge.amount_usd,
                "token": edge.token,
                "tx_signature": edge.tx_signature,
                "block_time": edge.block_time,
                "metadata": dict(edge.metadata),
            }
        )

    self.metadata.touch()

    return edge


def remove_edge(
    self,
    edge_id: EdgeId,
) -> bool:
    """
    Remove an edge from the graph.
    """

    edge = self.get_edge(edge_id)

    if edge is None:
        return False

    if self.graph.has_edge(
        edge.source,
        edge.target,
        key=edge.id,
    ):
        self.graph.remove_edge(
            edge.source,
            edge.target,
            key=edge.id,
        )

    self.edges.pop(edge.id, None)

    if edge.source in self.node_edges:
        self.node_edges[edge.source].discard(edge.id)

    if edge.target in self.node_edges:
        self.node_edges[edge.target].discard(edge.id)

    if self.stats["edges"] > 0:
        self.stats["edges"] -= 1

    if self.metadata.edge_count > 0:
        self.metadata.edge_count -= 1

    self._degree_cache.pop(edge.source, None)
    self._degree_cache.pop(edge.target, None)

    self._centrality_cache.pop(edge.source, None)
    self._centrality_cache.pop(edge.target, None)

    self._path_cache.clear()

    self.metadata.touch()

    return True


def remove_all_edges(
    self,
    source: NodeId,
    target: Optional[NodeId] = None,
) -> int:
    """
    Remove all edges.

    If target is None:
        Removes every edge connected to source.

    Otherwise:
        Removes every edge between source and target.
    """

    removed = 0

    edge_ids = []

    for edge in list(self.edges.values()):

        if target is None:

            if edge.source == source or edge.target == source:
                edge_ids.append(edge.id)

        else:

            if (
                edge.source == source
                and edge.target == target
            ):
                edge_ids.append(edge.id)

    for edge_id in edge_ids:

        if self.remove_edge(edge_id):
            removed += 1

    return removed

# =====================================================
# Part 4A
# Graph Traversal Algorithms
# Breadth First Search (BFS)
# Depth First Search (DFS)
# =====================================================

from collections import deque


def bfs(
    self,
    start: NodeId,
    max_depth: Optional[int] = None,
) -> List[NodeId]:
    """
    Breadth-First Search.

    Returns the visitation order.
    """

    self._validate_node_id(start)

    if start not in self.nodes:
        raise KeyError(f"Unknown node '{start}'.")

    visited: Set[NodeId] = set()

    order: List[NodeId] = []

    queue = deque()

    queue.append((start, 0))

    while queue:

        node, depth = queue.popleft()

        if node in visited:
            continue

        visited.add(node)

        order.append(node)

        if max_depth is not None and depth >= max_depth:
            continue

        for neighbor in self.graph.successors(node):

            if neighbor not in visited:

                queue.append(
                    (
                        neighbor,
                        depth + 1,
                    )
                )

    return order


def bfs_edges(
    self,
    start: NodeId,
    max_depth: Optional[int] = None,
) -> List[GraphEdge]:
    """
    Returns every traversed edge using BFS.
    """

    self._validate_node_id(start)

    if start not in self.nodes:
        raise KeyError(f"Unknown node '{start}'.")

    visited: Set[NodeId] = set()

    edges: List[GraphEdge] = []

    queue = deque()

    queue.append((start, 0))

    while queue:

        node, depth = queue.popleft()

        if node in visited:
            continue

        visited.add(node)

        if max_depth is not None and depth >= max_depth:
            continue

        for neighbor in self.graph.successors(node):

            graph_edges = self.get_edges_between(
                node,
                neighbor,
            )

            edges.extend(graph_edges)

            if neighbor not in visited:

                queue.append(
                    (
                        neighbor,
                        depth + 1,
                    )
                )

    return edges


def dfs(
    self,
    start: NodeId,
) -> List[NodeId]:
    """
    Depth-First Search.

    Returns visitation order.
    """

    self._validate_node_id(start)

    if start not in self.nodes:
        raise KeyError(f"Unknown node '{start}'.")

    visited: Set[NodeId] = set()

    order: List[NodeId] = []

    stack: List[NodeId] = [start]

    while stack:

        node = stack.pop()

        if node in visited:
            continue

        visited.add(node)

        order.append(node)

        neighbors = list(
            self.graph.successors(node)
        )

        neighbors.reverse()

        for neighbor in neighbors:

            if neighbor not in visited:

                stack.append(neighbor)

    return order


def dfs_edges(
    self,
    start: NodeId,
) -> List[GraphEdge]:
    """
    DFS edge traversal.
    """

    self._validate_node_id(start)

    if start not in self.nodes:
        raise KeyError(f"Unknown node '{start}'.")

    visited: Set[NodeId] = set()

    traversed: List[GraphEdge] = []

    stack: List[NodeId] = [start]

    while stack:

        node = stack.pop()

        if node in visited:
            continue

        visited.add(node)

        neighbors = list(
            self.graph.successors(node)
        )

        neighbors.reverse()

        for neighbor in neighbors:

            traversed.extend(
                self.get_edges_between(
                    node,
                    neighbor,
                )
            )

            if neighbor not in visited:

                stack.append(neighbor)

    return traversed


def reachable_nodes(
    self,
    start: NodeId,
) -> Set[NodeId]:
    """
    Returns every node reachable
    from start.
    """

    return set(
        self.bfs(start)
    )


def traversal_tree(
    self,
    start: NodeId,
) -> nx.DiGraph:
    """
    Build a traversal tree using BFS.
    """

    self._validate_node_id(start)

    tree = nx.DiGraph()

    visited: Set[NodeId] = set()

    queue = deque([start])

    while queue:

        current = queue.popleft()

        if current in visited:
            continue

        visited.add(current)

        tree.add_node(current)

        for neighbor in self.graph.successors(current):

            tree.add_edge(
                current,
                neighbor,
            )

            if neighbor not in visited:

                queue.append(neighbor)

    return tree

# =====================================================
# Part 4B
# Path Algorithms
# =====================================================

def shortest_path(
    self,
    source: NodeId,
    target: NodeId,
) -> List[NodeId]:
    """
    Compute the shortest path between two nodes.
    """

    self._validate_node_id(source)
    self._validate_node_id(target)

    if source not in self.nodes:
        raise KeyError(f"Unknown source node '{source}'.")

    if target not in self.nodes:
        raise KeyError(f"Unknown target node '{target}'.")

    cache_key = (source, target)

    if cache_key in self._path_cache:
        return list(self._path_cache[cache_key])

    try:
        path = nx.shortest_path(
            self.graph,
            source=source,
            target=target,
        )

        self._path_cache[cache_key] = list(path)

        return list(path)

    except nx.NetworkXNoPath:
        return []


def shortest_path_length(
    self,
    source: NodeId,
    target: NodeId,
) -> Optional[int]:
    """
    Returns the number of hops in the shortest path.
    """

    path = self.shortest_path(
        source,
        target,
    )

    if not path:
        return None

    return max(len(path) - 1, 0)


def path_exists(
    self,
    source: NodeId,
    target: NodeId,
) -> bool:
    """
    Returns True if a path exists.
    """

    return len(
        self.shortest_path(
            source,
            target,
        )
    ) > 0


def all_shortest_paths(
    self,
    source: NodeId,
    target: NodeId,
) -> List[List[NodeId]]:
    """
    Return every shortest path.
    """

    self._validate_node_id(source)
    self._validate_node_id(target)

    try:

        return list(
            nx.all_shortest_paths(
                self.graph,
                source,
                target,
            )
        )

    except nx.NetworkXNoPath:

        return []


def find_all_paths(
    self,
    source: NodeId,
    target: NodeId,
    cutoff: Optional[int] = None,
) -> List[List[NodeId]]:
    """
    Return all simple paths.

    cutoff limits maximum path length.
    """

    self._validate_node_id(source)
    self._validate_node_id(target)

    try:

        return list(
            nx.all_simple_paths(
                self.graph,
                source,
                target,
                cutoff=cutoff,
            )
        )

    except nx.NetworkXNoPath:

        return []


def shortest_path_edges(
    self,
    source: NodeId,
    target: NodeId,
) -> List[GraphEdge]:
    """
    Return GraphEdge objects along
    the shortest path.
    """

    path = self.shortest_path(
        source,
        target,
    )

    if len(path) < 2:
        return []

    result: List[GraphEdge] = []

    for i in range(len(path) - 1):

        result.extend(
            self.get_edges_between(
                path[i],
                path[i + 1],
            )
        )

    return result


def path_distance(
    self,
    source: NodeId,
    target: NodeId,
) -> float:
    """
    Weighted shortest path distance.
    """

    try:

        return nx.shortest_path_length(
            self.graph,
            source,
            target,
            weight="weight",
        )

    except nx.NetworkXNoPath:

        return float("inf")

# =====================================================
# Part 4C
# Connected Components
# =====================================================

def connected_components(
    self,
) -> List[Set[NodeId]]:
    """
    Return connected components.

    Since Wallet DNA uses a directed graph,
    this returns components from the undirected
    view of the graph.
    """

    graph = self.graph.to_undirected()

    return [
        set(component)
        for component in nx.connected_components(graph)
    ]


def connected_component_count(
    self,
) -> int:
    """
    Total connected components.
    """

    return len(
        self.connected_components()
    )


def strongly_connected_components(
    self,
) -> List[Set[NodeId]]:
    """
    Strongly Connected Components (SCC).

    Every node can reach every other node.
    """

    return [
        set(component)
        for component in nx.strongly_connected_components(
            self.graph
        )
    ]


def strongly_connected_component_count(
    self,
) -> int:
    """
    Number of SCCs.
    """

    return len(
        self.strongly_connected_components()
    )


def weakly_connected_components(
    self,
) -> List[Set[NodeId]]:
    """
    Weakly Connected Components (WCC).

    Direction of edges is ignored.
    """

    return [
        set(component)
        for component in nx.weakly_connected_components(
            self.graph
        )
    ]


def weakly_connected_component_count(
    self,
) -> int:
    """
    Number of weakly connected components.
    """

    return len(
        self.weakly_connected_components()
    )


def largest_component(
    self,
) -> Set[NodeId]:
    """
    Return the largest connected component.
    """

    components = self.connected_components()

    if not components:
        return set()

    return max(
        components,
        key=len,
    )


def component_of_node(
    self,
    node_id: NodeId,
) -> Set[NodeId]:
    """
    Return the connected component
    containing a node.
    """

    self._validate_node_id(node_id)

    if node_id not in self.nodes:
        raise KeyError(
            f"Unknown node '{node_id}'."
        )

    for component in self.connected_components():

        if node_id in component:

            return component

    return set()


def nodes_in_same_component(
    self,
    node_a: NodeId,
    node_b: NodeId,
) -> bool:
    """
    Returns True if both nodes belong
    to the same connected component.
    """

    component = self.component_of_node(node_a)

    return node_b in component


def isolated_nodes(
    self,
) -> List[NodeId]:
    """
    Return nodes with no connections.
    """

    return [
        node
        for node in self.graph.nodes()
        if self.graph.degree(node) == 0
    ]                        

# =====================================================
# Part 4D-1
# Degree Centrality
# =====================================================

def degree_centrality(
    self,
    use_cache: bool = True,
) -> Dict[NodeId, float]:
    """
    Compute degree centrality for every node.

    Parameters
    ----------
    use_cache : bool
        Use cached values if available.

    Returns
    -------
    Dict[NodeId, float]
    """

    if use_cache and self._centrality_cache:

        return dict(self._centrality_cache)

    centrality = nx.degree_centrality(
        self.graph
    )

    self._centrality_cache.clear()

    self._centrality_cache.update(
        centrality
    )

    return dict(centrality)


def node_degree_centrality(
    self,
    node_id: NodeId,
    use_cache: bool = True,
) -> float:
    """
    Degree centrality of a single node.
    """

    self._validate_node_id(node_id)

    if node_id not in self.nodes:
        raise KeyError(
            f"Unknown node '{node_id}'."
        )

    if (
        use_cache
        and node_id in self._centrality_cache
    ):
        return self._centrality_cache[node_id]

    values = self.degree_centrality(
        use_cache=False
    )

    return values.get(node_id, 0.0)


def degree_ranking(
    self,
    descending: bool = True,
) -> List[Tuple[NodeId, float]]:
    """
    Rank nodes by degree centrality.
    """

    values = self.degree_centrality()

    return sorted(
        values.items(),
        key=lambda item: item[1],
        reverse=descending,
    )


def top_degree_nodes(
    self,
    limit: int = 10,
) -> List[Tuple[WalletNode, float]]:
    """
    Return highest degree nodes.
    """

    ranking = self.degree_ranking()

    result: List[
        Tuple[WalletNode, float]
    ] = []

    for node_id, score in ranking[:limit]:

        node = self.get_node(node_id)

        if node is not None:

            result.append(
                (
                    node,
                    score,
                )
            )

    return result


def average_degree_centrality(
    self,
) -> float:
    """
    Average degree centrality.
    """

    values = self.degree_centrality()

    if not values:
        return 0.0

    return sum(values.values()) / len(values)


def highest_degree_node(
    self,
) -> Optional[WalletNode]:
    """
    Return the node with the highest
    degree centrality.
    """

    ranking = self.degree_ranking()

    if not ranking:
        return None

    node_id, _ = ranking[0]

    return self.get_node(node_id)


def lowest_degree_node(
    self,
) -> Optional[WalletNode]:
    """
    Return the node with the lowest
    degree centrality.
    """

    ranking = self.degree_ranking(
        descending=False
    )

    if not ranking:
        return None

    node_id, _ = ranking[0]

    return self.get_node(node_id)    

# =====================================================
# Part 4D-2
# Betweenness Centrality
# =====================================================

def betweenness_centrality(
    self,
    normalized: bool = True,
    use_cache: bool = False,
) -> Dict[NodeId, float]:
    """
    Compute betweenness centrality for every node.

    Parameters
    ----------
    normalized : bool
        Normalize scores.

    use_cache : bool
        Reserved for future caching support.
    """

    return nx.betweenness_centrality(
        self.graph,
        normalized=normalized,
        weight=None,
    )


def node_betweenness(
    self,
    node_id: NodeId,
    normalized: bool = True,
) -> float:
    """
    Betweenness centrality of a single node.
    """

    self._validate_node_id(node_id)

    if node_id not in self.nodes:
        raise KeyError(
            f"Unknown node '{node_id}'."
        )

    values = self.betweenness_centrality(
        normalized=normalized
    )

    return values.get(node_id, 0.0)


def betweenness_ranking(
    self,
    normalized: bool = True,
    descending: bool = True,
) -> List[Tuple[NodeId, float]]:
    """
    Rank nodes by betweenness centrality.
    """

    values = self.betweenness_centrality(
        normalized=normalized
    )

    return sorted(
        values.items(),
        key=lambda item: item[1],
        reverse=descending,
    )


def top_betweenness_nodes(
    self,
    limit: int = 10,
    normalized: bool = True,
) -> List[Tuple[WalletNode, float]]:
    """
    Return nodes with the highest betweenness.
    """

    ranking = self.betweenness_ranking(
        normalized=normalized
    )

    result: List[
        Tuple[WalletNode, float]
    ] = []

    for node_id, score in ranking[:limit]:

        node = self.get_node(node_id)

        if node is not None:

            result.append(
                (
                    node,
                    score,
                )
            )

    return result


def highest_betweenness_node(
    self,
) -> Optional[WalletNode]:
    """
    Node with highest betweenness.
    """

    ranking = self.betweenness_ranking()

    if not ranking:
        return None

    return self.get_node(
        ranking[0][0]
    )


def average_betweenness(
    self,
) -> float:
    """
    Average betweenness centrality.
    """

    values = self.betweenness_centrality()

    if not values:
        return 0.0

    return (
        sum(values.values())
        / len(values)
    )


def bridge_wallets(
    self,
    threshold: float = 0.05,
) -> List[WalletNode]:
    """
    Return wallets acting as bridges
    between clusters.
    """

    values = self.betweenness_centrality()

    result: List[WalletNode] = []

    for node_id, score in values.items():

        if score >= threshold:

            node = self.get_node(node_id)

            if node is not None:

                result.append(node)

    return result

# =====================================================
# Part 4D-3
# Closeness Centrality
# =====================================================

def closeness_centrality(
    self,
    use_cache: bool = False,
) -> Dict[NodeId, float]:
    """
    Compute closeness centrality for every node.

    Closeness measures how quickly a node can
    reach every other node in the graph.
    """

    return nx.closeness_centrality(
        self.graph
    )


def node_closeness(
    self,
    node_id: NodeId,
) -> float:
    """
    Closeness centrality of a single node.
    """

    self._validate_node_id(node_id)

    if node_id not in self.nodes:
        raise KeyError(
            f"Unknown node '{node_id}'."
        )

    values = self.closeness_centrality()

    return values.get(node_id, 0.0)


def closeness_ranking(
    self,
    descending: bool = True,
) -> List[Tuple[NodeId, float]]:
    """
    Rank nodes by closeness centrality.
    """

    values = self.closeness_centrality()

    return sorted(
        values.items(),
        key=lambda item: item[1],
        reverse=descending,
    )


def top_closeness_nodes(
    self,
    limit: int = 10,
) -> List[Tuple[WalletNode, float]]:
    """
    Return highest closeness nodes.
    """

    ranking = self.closeness_ranking()

    result: List[
        Tuple[WalletNode, float]
    ] = []

    for node_id, score in ranking[:limit]:

        node = self.get_node(node_id)

        if node is not None:

            result.append(
                (
                    node,
                    score,
                )
            )

    return result


def highest_closeness_node(
    self,
) -> Optional[WalletNode]:
    """
    Return the node with the highest
    closeness centrality.
    """

    ranking = self.closeness_ranking()

    if not ranking:
        return None

    return self.get_node(
        ranking[0][0]
    )


def average_closeness(
    self,
) -> float:
    """
    Average closeness centrality.
    """

    values = self.closeness_centrality()

    if not values:
        return 0.0

    return (
        sum(values.values())
        / len(values)
    )


def closest_wallets(
    self,
    threshold: float = 0.50,
) -> List[WalletNode]:
    """
    Return wallets having high
    closeness centrality.
    """

    values = self.closeness_centrality()

    wallets: List[WalletNode] = []

    for node_id, score in values.items():

        if score >= threshold:

            node = self.get_node(node_id)

            if node is not None:

                wallets.append(node)

    return wallets


def closeness_statistics(
    self,
) -> Dict[str, float]:
    """
    Summary statistics for closeness.
    """

    values = list(
        self.closeness_centrality().values()
    )

    if not values:

        return {
            "min": 0.0,
            "max": 0.0,
            "avg": 0.0,
        }

    return {
        "min": min(values),
        "max": max(values),
        "avg": sum(values) / len(values),
    }

# =====================================================
# Part 4D-4
# PageRank
# =====================================================

def pagerank(
    self,
    alpha: float = 0.85,
    max_iter: int = 100,
    tol: float = 1.0e-6,
) -> Dict[NodeId, float]:
    """
    Compute PageRank for every node.

    Parameters
    ----------
    alpha
        Damping factor.

    max_iter
        Maximum iterations.

    tol
        Error tolerance.
    """

    return nx.pagerank(
        self.graph,
        alpha=alpha,
        max_iter=max_iter,
        tol=tol,
        weight="weight",
    )


def node_pagerank(
    self,
    node_id: NodeId,
    alpha: float = 0.85,
) -> float:
    """
    PageRank score for one node.
    """

    self._validate_node_id(node_id)

    if node_id not in self.nodes:
        raise KeyError(
            f"Unknown node '{node_id}'."
        )

    values = self.pagerank(
        alpha=alpha,
    )

    return values.get(
        node_id,
        0.0,
    )


def pagerank_ranking(
    self,
    alpha: float = 0.85,
    descending: bool = True,
) -> List[Tuple[NodeId, float]]:
    """
    Rank nodes by PageRank.
    """

    values = self.pagerank(
        alpha=alpha,
    )

    return sorted(
        values.items(),
        key=lambda item: item[1],
        reverse=descending,
    )


def top_pagerank_nodes(
    self,
    limit: int = 10,
    alpha: float = 0.85,
) -> List[Tuple[WalletNode, float]]:
    """
    Return top PageRank nodes.
    """

    ranking = self.pagerank_ranking(
        alpha=alpha,
    )

    result: List[
        Tuple[WalletNode, float]
    ] = []

    for node_id, score in ranking[:limit]:

        node = self.get_node(node_id)

        if node is not None:

            result.append(
                (
                    node,
                    score,
                )
            )

    return result


def highest_pagerank_node(
    self,
    alpha: float = 0.85,
) -> Optional[WalletNode]:
    """
    Return highest PageRank node.
    """

    ranking = self.pagerank_ranking(
        alpha=alpha,
    )

    if not ranking:
        return None

    return self.get_node(
        ranking[0][0]
    )


def average_pagerank(
    self,
    alpha: float = 0.85,
) -> float:
    """
    Average PageRank.
    """

    values = self.pagerank(
        alpha=alpha,
    )

    if not values:
        return 0.0

    return (
        sum(values.values())
        / len(values)
    )


def top_central_nodes(
    self,
    limit: int = 10,
) -> List[Dict[str, Any]]:
    """
    Return the most important nodes using
    multiple graph centrality metrics.
    """

    degree = self.degree_centrality()

    between = self.betweenness_centrality()

    close = self.closeness_centrality()

    rank = self.pagerank()

    scores: List[
        Dict[str, Any]
    ] = []

    for node_id in self.nodes:

        node = self.get_node(node_id)

        if node is None:
            continue

        composite = (
            degree.get(node_id, 0.0)
            + between.get(node_id, 0.0)
            + close.get(node_id, 0.0)
            + rank.get(node_id, 0.0)
        ) / 4.0

        scores.append(
            {
                "node": node,
                "node_id": node_id,
                "degree": degree.get(node_id, 0.0),
                "betweenness": between.get(node_id, 0.0),
                "closeness": close.get(node_id, 0.0),
                "pagerank": rank.get(node_id, 0.0),
                "score": composite,
            }
        )

    scores.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return scores[:limit]

# =====================================================
# Part 5A
# Dictionary Serialization
# =====================================================

def to_dict(self) -> Dict[str, Any]:
    """
    Serialize the entire graph into a dictionary.
    """

    self.update_metadata()

    return {
        "metadata": self.metadata.to_dict(),
        "nodes": [
            node.to_dict()
            for node in self.nodes.values()
        ],
        "edges": [
            edge.to_dict()
            for edge in self.edges.values()
        ],
    }


@classmethod
def from_dict(
    cls,
    data: Dict[str, Any],
) -> "GraphBuilder":
    """
    Reconstruct a GraphBuilder from a serialized dictionary.
    """

    if not isinstance(data, dict):
        raise TypeError(
            "data must be a dictionary."
        )

    metadata = data.get("metadata", {})

    graph = cls(
        name=metadata.get(
            "graph_name",
            DEFAULT_GRAPH_NAME,
        )
    )

    # ------------------------------------------
    # Restore Metadata
    # ------------------------------------------

    graph.metadata.version = metadata.get(
        "version",
        GRAPH_VERSION,
    )

    graph.metadata.description = metadata.get(
        "description",
        "",
    )

    graph.metadata.status = GraphStatus(
        metadata.get(
            "status",
            GraphStatus.READY.value,
        )
    )

    graph.metadata.metadata = metadata.get(
        "metadata",
        {},
    )

    # ------------------------------------------
    # Restore Nodes
    # ------------------------------------------

    for item in data.get("nodes", []):

        node = WalletNode(
            id=item["id"],
            address=item["address"],
            node_type=NodeType(
                item["node_type"]
            ),
            label=WalletLabel(
                item["label"]
            ),
            name=item.get("name"),
            tags=item.get(
                "tags",
                [],
            ),
            risk_level=RiskLevel(
                item.get(
                    "risk_level",
                    RiskLevel.LOW.value,
                )
            ),
            risk_score=item.get(
                "risk_score",
                0.0,
            ),
            similarity_score=item.get(
                "similarity_score",
                0.0,
            ),
            confidence=item.get(
                "confidence",
                1.0,
            ),
            balance_sol=item.get(
                "balance_sol",
                0.0,
            ),
            usd_value=item.get(
                "usd_value",
                0.0,
            ),
            tx_count=item.get(
                "tx_count",
                0,
            ),
            token_count=item.get(
                "token_count",
                0,
            ),
            first_seen=datetime.fromisoformat(
                item["first_seen"]
            ),
            last_seen=datetime.fromisoformat(
                item["last_seen"]
            ),
            metadata=item.get(
                "metadata",
                {},
            ),
        )

        graph.add_node(node)

    # ------------------------------------------
    # Restore Edges
    # ------------------------------------------

    for item in data.get("edges", []):

        edge = GraphEdge(
            id=item["id"],
            source=item["source"],
            target=item["target"],
            edge_type=EdgeType(
                item["edge_type"]
            ),
            weight=item.get(
                "weight",
                1.0,
            ),
            confidence=item.get(
                "confidence",
                1.0,
            ),
            amount_sol=item.get(
                "amount_sol",
                0.0,
            ),
            amount_usd=item.get(
                "amount_usd",
                0.0,
            ),
            token=item.get("token"),
            tx_signature=item.get(
                "tx_signature"
            ),
            block_time=datetime.fromisoformat(
                item["block_time"]
            ),
            metadata=item.get(
                "metadata",
                {},
            ),
        )

        graph.add_edge(edge)

    graph.update_metadata()

    return graph

# =====================================================
# Part 5B
# JSON Serialization
# =====================================================

import json
from pathlib import Path


def to_json(
    self,
    *,
    indent: int = 4,
    sort_keys: bool = False,
) -> str:
    """
    Serialize the graph to a JSON string.

    Parameters
    ----------
    indent
        Pretty-print indentation.

    sort_keys
        Sort JSON keys.

    Returns
    -------
    str
    """

    return json.dumps(
        self.to_dict(),
        indent=indent,
        sort_keys=sort_keys,
    )


@classmethod
def from_json(
    cls,
    json_data: str,
) -> "GraphBuilder":
    """
    Construct a GraphBuilder from JSON.
    """

    if not isinstance(json_data, str):
        raise TypeError(
            "json_data must be a string."
        )

    try:

        data = json.loads(json_data)

    except json.JSONDecodeError as exc:

        raise ValueError(
            "Invalid JSON."
        ) from exc

    return cls.from_dict(data)


def save_json(
    self,
    filepath: str | Path,
    *,
    indent: int = 4,
    sort_keys: bool = False,
) -> Path:
    """
    Save graph as JSON.

    Returns
    -------
    Path
        Saved file path.
    """

    path = Path(filepath)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        self.to_json(
            indent=indent,
            sort_keys=sort_keys,
        ),
        encoding="utf-8",
    )

    return path


@classmethod
def load_json(
    cls,
    filepath: str | Path,
) -> "GraphBuilder":
    """
    Load graph from JSON file.
    """

    path = Path(filepath)

    if not path.exists():

        raise FileNotFoundError(path)

    return cls.from_json(
        path.read_text(
            encoding="utf-8",
        )
    )


def export_json(
    self,
    filepath: str | Path,
) -> Path:
    """
    Alias of save_json().
    """

    return self.save_json(filepath)


@classmethod
def import_json(
    cls,
    filepath: str | Path,
) -> "GraphBuilder":
    """
    Alias of load_json().
    """

    return cls.load_json(filepath)

# =====================================================
# GraphML / GEXF Serialization Helpers
# =====================================================

def _graphml_safe_value(
    self,
    value: Any,
) -> Any:
    """
    Convert Python objects into GraphML/GEXF-safe values.
    """

    if value is None:
        return ""

    if isinstance(
        value,
        (str, int, float, bool),
    ):
        return value

    if isinstance(value, Enum):
        return value.value

    if isinstance(value, datetime):
        return value.isoformat()

    if isinstance(
        value,
        (
            list,
            tuple,
            set,
        ),
    ):
        return json.dumps(
            list(value)
        )

    if isinstance(
        value,
        dict,
    ):
        return json.dumps(value)

    return str(value)


def _graphml_safe_attributes(
    self,
    attributes: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Convert an attribute dictionary into
    GraphML-compatible attributes.
    """

    safe: Dict[str, Any] = {}

    for key, value in attributes.items():

        safe[key] = self._graphml_safe_value(
            value
        )

    return safe


def _restore_graphml_attributes(
    self,
    attributes: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Restore JSON-encoded values exported
    by GraphML/GEXF.
    """

    restored: Dict[str, Any] = {}

    for key, value in attributes.items():

        if not isinstance(value, str):

            restored[key] = value

            continue

        text = value.strip()

        if not text:

            restored[key] = ""

            continue

        if text.startswith("{") or text.startswith("["):

            try:

                restored[key] = json.loads(text)

                continue

            except Exception:

                pass

        restored[key] = value

    return restored


def _graphml_node_attributes(
    self,
    node: WalletNode,
) -> Dict[str, Any]:
    """
    Convert WalletNode into GraphML-safe attributes.
    """

    return self._graphml_safe_attributes(
        node.to_dict()
    )


def _graphml_edge_attributes(
    self,
    edge: GraphEdge,
) -> Dict[str, Any]:
    """
    Convert GraphEdge into GraphML-safe attributes.
    """

    return self._graphml_safe_attributes(
        edge.to_dict()
    )

# =====================================================
# Part 5C-1
# GraphML Export
# =====================================================

from pathlib import Path


def to_graphml(
    self,
    filepath: str | Path,
) -> Path:
    """
    Export the Wallet DNA graph to GraphML.

    The exported graph is compatible with:

    • Gephi
    • Cytoscape
    • Neo4j Import
    • yEd
    • NetworkX

    Returns
    -------
    Path
        Saved file path.
    """

    path = Path(filepath)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    export_graph = nx.MultiDiGraph(
        name=self.graph_name
    )

    # --------------------------------------------------
    # Export Nodes
    # --------------------------------------------------

    for node in self.nodes.values():

        export_graph.add_node(
            node.id,
            **self._graphml_node_attributes(node),
        )

    # --------------------------------------------------
    # Export Edges
    # --------------------------------------------------

    for edge in self.edges.values():

        export_graph.add_edge(
            edge.source,
            edge.target,
            key=edge.id,
            **self._graphml_edge_attributes(edge),
        )

    # --------------------------------------------------
    # Graph Metadata
    # --------------------------------------------------

    export_graph.graph.update(
        self._graphml_safe_attributes(
            self.metadata.to_dict()
        )
    )

    # --------------------------------------------------
    # Write File
    # --------------------------------------------------

    nx.write_graphml(
        export_graph,
        path,
    )

    return path

# =====================================================
# Part 5C-2A
# GraphML Import
# Read File
# Create GraphBuilder
# Restore Metadata
# =====================================================

@classmethod
def from_graphml(
    cls,
    filepath: str | Path,
) -> "GraphBuilder":
    """
    Load a GraphBuilder from a GraphML file.

    This method restores:

    • Graph metadata
    • Wallet nodes (Part 5C-2B)
    • Graph edges (Part 5C-2C)
    """

    path = Path(filepath)

    if not path.exists():
        raise FileNotFoundError(path)

    # --------------------------------------------------
    # Read GraphML
    # --------------------------------------------------

    graphml = nx.read_graphml(path)

    if not isinstance(
        graphml,
        (
            nx.Graph,
            nx.DiGraph,
            nx.MultiGraph,
            nx.MultiDiGraph,
        ),
    ):
        raise TypeError(
            "Invalid GraphML graph."
        )

    # --------------------------------------------------
    # Restore Graph Metadata
    # --------------------------------------------------

    metadata = {}

    if hasattr(graphml, "graph"):

        metadata = graphml.graph.copy()

    metadata = cls()._restore_graphml_attributes(
        metadata
    )

    builder = cls(
        name=metadata.get(
            "graph_name",
            DEFAULT_GRAPH_NAME,
        )
    )

    builder.metadata.version = metadata.get(
        "version",
        GRAPH_VERSION,
    )

    builder.metadata.description = metadata.get(
        "description",
        "",
    )

    if "status" in metadata:

        builder.metadata.status = GraphStatus(
            metadata["status"]
        )

    builder.metadata.metadata = metadata.get(
        "metadata",
        {},
    )

    builder.metadata.created_at = datetime.fromisoformat(
        metadata.get(
            "created_at",
            datetime.utcnow().isoformat(),
        )
    )

    builder.metadata.updated_at = datetime.fromisoformat(
        metadata.get(
            "updated_at",
            datetime.utcnow().isoformat(),
        )
    )

    return builder   

    # --------------------------------------------------
    # Part 5C-2B
    # Restore Wallet Nodes
    # --------------------------------------------------

    for node_id, attributes in graphml.nodes(data=True):

        attributes = builder._restore_graphml_attributes(
            dict(attributes)
        )

        node = WalletNode(
            id=attributes.get(
                "id",
                node_id,
            ),
            address=attributes.get(
                "address",
                "",
            ),
            node_type=NodeType(
                attributes.get(
                    "node_type",
                    NodeType.WALLET.value,
                )
            ),
            label=WalletLabel(
                attributes.get(
                    "label",
                    WalletLabel.NORMAL.value,
                )
            ),
            name=attributes.get(
                "name",
            ),
            tags=attributes.get(
                "tags",
                [],
            ),
            risk_level=RiskLevel(
                attributes.get(
                    "risk_level",
                    RiskLevel.LOW.value,
                )
            ),
            risk_score=float(
                attributes.get(
                    "risk_score",
                    DEFAULT_RISK_SCORE,
                )
            ),
            similarity_score=float(
                attributes.get(
                    "similarity_score",
                    DEFAULT_SIMILARITY_SCORE,
                )
            ),
            confidence=float(
                attributes.get(
                    "confidence",
                    DEFAULT_CONFIDENCE,
                )
            ),
            balance_sol=float(
                attributes.get(
                    "balance_sol",
                    0.0,
                )
            ),
            usd_value=float(
                attributes.get(
                    "usd_value",
                    0.0,
                )
            ),
            tx_count=int(
                attributes.get(
                    "tx_count",
                    0,
                )
            ),
            token_count=int(
                attributes.get(
                    "token_count",
                    0,
                )
            ),
            first_seen=datetime.fromisoformat(
                attributes.get(
                    "first_seen",
                    now().isoformat(),
                )
            ),
            last_seen=datetime.fromisoformat(
                attributes.get(
                    "last_seen",
                    now().isoformat(),
                )
            ),
            metadata=attributes.get(
                "metadata",
                {},
            ),
        )

        builder.add_node(node)
                     

    # --------------------------------------------------
    # Part 5C-2C
    # Restore Graph Edges
    # --------------------------------------------------

    if graphml.is_multigraph():

        edge_iterator = graphml.edges(
            keys=True,
            data=True,
        )

        for source, target, key, attributes in edge_iterator:

            attributes = builder._restore_graphml_attributes(
                dict(attributes)
            )

            edge = GraphEdge(
                id=attributes.get(
                    "id",
                    str(key),
                ),
                source=source,
                target=target,
                edge_type=EdgeType(
                    attributes.get(
                        "edge_type",
                        EdgeType.TRANSFER.value,
                    )
                ),
                weight=float(
                    attributes.get(
                        "weight",
                        DEFAULT_EDGE_WEIGHT,
                    )
                ),
                confidence=float(
                    attributes.get(
                        "confidence",
                        DEFAULT_CONFIDENCE,
                    )
                ),
                amount_sol=float(
                    attributes.get(
                        "amount_sol",
                        0.0,
                    )
                ),
                amount_usd=float(
                    attributes.get(
                        "amount_usd",
                        0.0,
                    )
                ),
                token=attributes.get(
                    "token",
                ),
                tx_signature=attributes.get(
                    "tx_signature",
                ),
                block_time=datetime.fromisoformat(
                    attributes.get(
                        "block_time",
                        now().isoformat(),
                    )
                ),
                metadata=attributes.get(
                    "metadata",
                    {},
                ),
            )

            builder.add_edge(edge)

    else:

        edge_iterator = graphml.edges(
            data=True,
        )

        for source, target, attributes in edge_iterator:

            attributes = builder._restore_graphml_attributes(
                dict(attributes)
            )

            edge = GraphEdge(
                id=attributes.get(
                    "id",
                    str(uuid.uuid4()),
                ),
                source=source,
                target=target,
                edge_type=EdgeType(
                    attributes.get(
                        "edge_type",
                        EdgeType.TRANSFER.value,
                    )
                ),
                weight=float(
                    attributes.get(
                        "weight",
                        DEFAULT_EDGE_WEIGHT,
                    )
                ),
                confidence=float(
                    attributes.get(
                        "confidence",
                        DEFAULT_CONFIDENCE,
                    )
                ),
                amount_sol=float(
                    attributes.get(
                        "amount_sol",
                        0.0,
                    )
                ),
                amount_usd=float(
                    attributes.get(
                        "amount_usd",
                        0.0,
                    )
                ),
                token=attributes.get(
                    "token",
                ),
                tx_signature=attributes.get(
                    "tx_signature",
                ),
                block_time=datetime.fromisoformat(
                    attributes.get(
                        "block_time",
                        now().isoformat(),
                    )
                ),
                metadata=attributes.get(
                    "metadata",
                    {},
                ),
            )

            builder.add_edge(edge)

    # --------------------------------------------------
    # Part 5C-2D
    # Finalize Graph
    # --------------------------------------------------

    # ------------------------------------------
    # Rebuild Node/Edge Indexes
    # ------------------------------------------

    builder.node_index.clear()

    for node_id, node in builder.nodes.items():

        builder.node_index[node.address] = node_id

    builder.edge_index.clear()

    for edge_id, edge in builder.edges.items():

        builder.edge_index[(
            edge.source,
            edge.target,
            edge.edge_type,
        )] = edge_id

    # ------------------------------------------
    # Rebuild Neighbor Cache
    # ------------------------------------------

    builder._neighbors_cache.clear()

    for node_id in builder.graph.nodes():

        builder._neighbors_cache[node_id] = set(
            builder.graph.neighbors(node_id)
        )

    # ------------------------------------------
    # Clear Algorithm Caches
    # ------------------------------------------

    builder._centrality_cache.clear()

    builder._pagerank_cache.clear()

    builder._path_cache.clear()

    # ------------------------------------------
    # Validate Graph
    # ------------------------------------------

    if len(builder.nodes) != builder.graph.number_of_nodes():

        raise RuntimeError(
            "Node count mismatch after GraphML import."
        )

    if len(builder.edges) != builder.graph.number_of_edges():

        raise RuntimeError(
            "Edge count mismatch after GraphML import."
        )

    # ------------------------------------------
    # Update Metadata
    # ------------------------------------------

    builder.update_metadata()

    builder.metadata.updated_at = now()

    # ------------------------------------------
    # Return GraphBuilder
    # ------------------------------------------

    return builder        