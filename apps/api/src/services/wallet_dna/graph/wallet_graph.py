###############################################################################
# Imports
###############################################################################

from __future__ import annotations

import copy
import json
import logging
import time
import uuid

from collections import (
    defaultdict,
    deque,
)

from dataclasses import (
    dataclass,
    field,
)

from enum import (
    Enum,
    IntEnum,
    auto,
)

from pathlib import Path

from typing import (
    Any,
    Deque,
    DefaultDict,
    Dict,
    FrozenSet,
    Iterable,
    Iterator,
    List,
    Optional,
    Set,
    Tuple,
    Union,
)

import networkx as nx


###############################################################################
# Constants
###############################################################################

GRAPH_NAME = "WalletDNA"

GRAPH_VERSION = "1.0.0"

DEFAULT_GRAPH_TYPE = "MultiDiGraph"

DEFAULT_NODE_CAPACITY = 5_000_000

DEFAULT_EDGE_CAPACITY = 50_000_000

DEFAULT_MAX_DEPTH = 50

DEFAULT_MAX_PATH_LENGTH = 100

DEFAULT_BATCH_SIZE = 1000

DEFAULT_CACHE_SIZE = 50000

DEFAULT_EXPORT_FORMAT = "json"


###############################################################################
# Enums
###############################################################################

class NodeType(Enum):
    """
    Graph node types.
    """

    WALLET = auto()

    TOKEN = auto()

    DEPLOYER = auto()

    BUNDLE = auto()

    CONTRACT = auto()

    UNKNOWN = auto()


###############################################################################


class EdgeType(Enum):
    """
    Graph edge types.
    """

    FUNDING = auto()

    TRANSFER = auto()

    DEPLOYMENT = auto()

    INTERACTION = auto()

    BUNDLE = auto()

    OWNERSHIP = auto()


###############################################################################


class TraversalMode(Enum):
    """
    Graph traversal mode.
    """

    BFS = auto()

    DFS = auto()

    SHORTEST_PATH = auto()


###############################################################################


class GraphState(Enum):
    """
    Graph lifecycle state.
    """

    INITIALIZING = auto()

    READY = auto()

    UPDATING = auto()

    OPTIMIZING = auto()

    CLOSED = auto()


###############################################################################
# Data Models
###############################################################################

@dataclass(slots=True)
class GraphNode:
    """
    Generic graph node.
    """

    node_id: str

    node_type: NodeType

    label: str

    metadata: Dict[str, Any] = field(
        default_factory=dict,
    )

    created_at: float = field(
        default_factory=time.time,
    )

    updated_at: float = field(
        default_factory=time.time,
    )


###############################################################################


@dataclass(slots=True)
class GraphEdge:
    """
    Generic graph edge.
    """

    source: str

    destination: str

    edge_type: EdgeType

    weight: float = 1.0

    metadata: Dict[str, Any] = field(
        default_factory=dict,
    )

    created_at: float = field(
        default_factory=time.time,
    )


###############################################################################


@dataclass(slots=True)
class GraphPath:
    """
    Represents a graph path.
    """

    nodes: List[str] = field(
        default_factory=list,
    )

    edges: List[GraphEdge] = field(
        default_factory=list,
    )

    distance: float = 0.0


###############################################################################


@dataclass(slots=True)
class GraphSnapshot:
    """
    Graph snapshot.
    """

    snapshot_id: str = field(
        default_factory=lambda: str(uuid.uuid4()),
    )

    timestamp: float = field(
        default_factory=time.time,
    )

    node_count: int = 0

    edge_count: int = 0

    metadata: Dict[str, Any] = field(
        default_factory=dict,
    )


###############################################################################
# WalletGraph
###############################################################################

class WalletGraph:
    """
    Core Wallet DNA Graph Engine.

    Responsible for:

    • Graph creation
    • Wallet nodes
    • Token nodes
    • Deployer nodes
    • Bundle nodes
    • Edge management
    • Traversal
    • Funding graph
    • Bundle graph
    • Deployer graph
    • Relationship discovery
    • Subgraphs
    • Graph analytics
    """
    

###############################################################################
# Initialization
###############################################################################

def __init__(
    self,
    config: Optional[Any] = None,
    logger: Optional[logging.Logger] = None,
):
    """
    Initialize Wallet DNA Graph.
    """

    ###########################################################################
    # Core
    ###########################################################################

    self.logger = logger or logging.getLogger(__name__)

    self.config = config

    self.graph_name = GRAPH_NAME

    self.graph_version = GRAPH_VERSION

    self.state = GraphState.INITIALIZING

    ###########################################################################
    # Initialization
    ###########################################################################

    self._initialize_graph()

    self._initialize_indexes()

    self._initialize_cache()

    self._initialize_configuration()

    ###########################################################################

    self.created_at = time.time()

    self.updated_at = self.created_at

    self.state = GraphState.READY

    self.logger.info(
        "WalletGraph initialized successfully."
    )


###############################################################################


def _initialize_graph(self) -> None:
    """
    Create underlying graph object.
    """

    self.graph: nx.MultiDiGraph = nx.MultiDiGraph()

    self.graph.graph["name"] = self.graph_name

    self.graph.graph["version"] = self.graph_version

    self.graph.graph["created_at"] = time.time()

    self.graph.graph["type"] = DEFAULT_GRAPH_TYPE


###############################################################################


def _initialize_indexes(self) -> None:
    """
    Create lookup indexes.
    """

    ###########################################################################
    # Node Indexes
    ###########################################################################

    self.wallet_index: Dict[str, str] = {}

    self.token_index: Dict[str, str] = {}

    self.deployer_index: Dict[str, str] = {}

    self.bundle_index: Dict[str, str] = {}

    ###########################################################################
    # Reverse Indexes
    ###########################################################################

    self.node_types: Dict[str, NodeType] = {}

    self.edge_types: Dict[
        Tuple[str, str],
        EdgeType,
    ] = {}

    ###########################################################################
    # Relationship Indexes
    ###########################################################################

    self.wallet_tokens: DefaultDict[
        str,
        Set[str],
    ] = defaultdict(set)

    self.token_wallets: DefaultDict[
        str,
        Set[str],
    ] = defaultdict(set)

    self.wallet_funding: DefaultDict[
        str,
        Set[str],
    ] = defaultdict(set)

    self.wallet_receivers: DefaultDict[
        str,
        Set[str],
    ] = defaultdict(set)


###############################################################################


def _initialize_cache(self) -> None:
    """
    Initialize in-memory caches.
    """

    self.node_cache: Dict[
        str,
        GraphNode,
    ] = {}

    self.edge_cache: Dict[
        Tuple[str, str],
        GraphEdge,
    ] = {}

    self.path_cache: Dict[
        Tuple[str, str],
        GraphPath,
    ] = {}

    self.subgraph_cache: Dict[
        str,
        nx.MultiDiGraph,
    ] = {}

    self.statistics_cache: Dict[
        str,
        Any,
    ] = {}

    self.cache_hits = 0

    self.cache_misses = 0


###############################################################################


def _initialize_configuration(self) -> None:
    """
    Initialize graph configuration.
    """

    self.max_nodes = DEFAULT_NODE_CAPACITY

    self.max_edges = DEFAULT_EDGE_CAPACITY

    self.max_depth = DEFAULT_MAX_DEPTH

    self.max_path_length = DEFAULT_MAX_PATH_LENGTH

    self.batch_size = DEFAULT_BATCH_SIZE

    self.cache_size = DEFAULT_CACHE_SIZE

    ###########################################################################

    if self.config is not None:

        try:

            graph_cfg = self.config.graph_settings()

            traversal_cfg = (
                self.config.traversal_settings()
            )

            cache_cfg = (
                self.config.cache_settings()
            )

            self.max_nodes = graph_cfg.max_nodes

            self.max_edges = graph_cfg.max_edges

            self.max_depth = (
                traversal_cfg.max_depth
            )

            self.max_path_length = (
                traversal_cfg.max_path_length
            )

            self.batch_size = (
                traversal_cfg.batch_size
            )

            self.cache_size = (
                cache_cfg.cache_size
            )

        except Exception:

            self.logger.warning(
                "Using default WalletGraph configuration."
            )

###############################################################################
# Node Management
###############################################################################

def add_wallet(
    self,
    wallet: str,
    metadata: Optional[Dict[str, Any]] = None,
) -> GraphNode:
    """
    Add a wallet node.
    """

    metadata = metadata or {}

    node = GraphNode(
        node_id=wallet,
        node_type=NodeType.WALLET,
        label=wallet,
        metadata=metadata,
    )

    self.graph.add_node(
        wallet,
        data=node,
    )

    self.wallet_index[wallet] = wallet
    self.node_types[wallet] = NodeType.WALLET
    self.node_cache[wallet] = node

    return node


###############################################################################


def add_token(
    self,
    token: str,
    metadata: Optional[Dict[str, Any]] = None,
) -> GraphNode:
    """
    Add token node.
    """

    metadata = metadata or {}

    node = GraphNode(
        node_id=token,
        node_type=NodeType.TOKEN,
        label=token,
        metadata=metadata,
    )

    self.graph.add_node(
        token,
        data=node,
    )

    self.token_index[token] = token
    self.node_types[token] = NodeType.TOKEN
    self.node_cache[token] = node

    return node


###############################################################################


def add_deployer(
    self,
    deployer: str,
    metadata: Optional[Dict[str, Any]] = None,
) -> GraphNode:
    """
    Add deployer node.
    """

    metadata = metadata or {}

    node = GraphNode(
        node_id=deployer,
        node_type=NodeType.DEPLOYER,
        label=deployer,
        metadata=metadata,
    )

    self.graph.add_node(
        deployer,
        data=node,
    )

    self.deployer_index[deployer] = deployer
    self.node_types[deployer] = NodeType.DEPLOYER
    self.node_cache[deployer] = node

    return node


###############################################################################


def add_bundle(
    self,
    bundle: str,
    metadata: Optional[Dict[str, Any]] = None,
) -> GraphNode:
    """
    Add bundle node.
    """

    metadata = metadata or {}

    node = GraphNode(
        node_id=bundle,
        node_type=NodeType.BUNDLE,
        label=bundle,
        metadata=metadata,
    )

    self.graph.add_node(
        bundle,
        data=node,
    )

    self.bundle_index[bundle] = bundle
    self.node_types[bundle] = NodeType.BUNDLE
    self.node_cache[bundle] = node

    return node


###############################################################################


def update_node(
    self,
    node_id: str,
    metadata: Dict[str, Any],
) -> bool:
    """
    Update node metadata.
    """

    if node_id not in self.graph:

        return False

    node = self.graph.nodes[node_id]["data"]

    node.metadata.update(metadata)

    node.updated_at = time.time()

    self.node_cache[node_id] = node

    return True


###############################################################################


def remove_node(
    self,
    node_id: str,
) -> bool:
    """
    Remove node.
    """

    if node_id not in self.graph:

        return False

    self.graph.remove_node(node_id)

    self.wallet_index.pop(node_id, None)

    self.token_index.pop(node_id, None)

    self.deployer_index.pop(node_id, None)

    self.bundle_index.pop(node_id, None)

    self.node_types.pop(node_id, None)

    self.node_cache.pop(node_id, None)

    return True


###############################################################################


def get_node(
    self,
    node_id: str,
) -> Optional[GraphNode]:
    """
    Return node object.
    """

    if node_id not in self.graph:

        return None

    return self.graph.nodes[node_id]["data"]


###############################################################################


def node_exists(
    self,
    node_id: str,
) -> bool:
    """
    Check node existence.
    """

    return node_id in self.graph


###############################################################################


def wallet_node(
    self,
    wallet: str,
) -> Optional[GraphNode]:
    """
    Return wallet node.
    """

    return self.get_node(wallet)


###############################################################################


def token_node(
    self,
    token: str,
) -> Optional[GraphNode]:
    """
    Return token node.
    """

    return self.get_node(token)


###############################################################################


def deployer_node(
    self,
    deployer: str,
) -> Optional[GraphNode]:
    """
    Return deployer node.
    """

    return self.get_node(deployer)

###############################################################################
# Edge Management
###############################################################################

def add_edge(
    self,
    source: str,
    destination: str,
    edge_type: EdgeType,
    weight: float = 1.0,
    metadata: Optional[Dict[str, Any]] = None,
) -> GraphEdge:
    """
    Add a graph edge.
    """

    metadata = metadata or {}

    edge = GraphEdge(
        source=source,
        destination=destination,
        edge_type=edge_type,
        weight=weight,
        metadata=metadata,
    )

    self.graph.add_edge(
        source,
        destination,
        key=edge_type.name,
        data=edge,
        weight=weight,
    )

    self.edge_cache[
        (source, destination, edge_type.name)
    ] = edge

    self.edge_types[
        (source, destination)
    ] = edge_type

    return edge


###############################################################################


def remove_edge(
    self,
    source: str,
    destination: str,
    edge_type: Optional[EdgeType] = None,
) -> bool:
    """
    Remove graph edge.
    """

    if not self.graph.has_edge(
        source,
        destination,
    ):
        return False

    try:

        if edge_type is None:

            self.graph.remove_edges_from(

                list(

                    self.graph.edges(

                        source,

                        keys=True,

                    )

                )

            )

        else:

            self.graph.remove_edge(

                source,

                destination,

                key=edge_type.name,

            )

        self.edge_cache.pop(

            (

                source,

                destination,

                edge_type.name if edge_type else "",

            ),

            None,

        )

        self.edge_types.pop(

            (source, destination),

            None,

        )

        return True

    except Exception:

        return False


###############################################################################


def update_edge(
    self,
    source: str,
    destination: str,
    edge_type: EdgeType,
    metadata: Dict[str, Any],
) -> bool:
    """
    Update edge metadata.
    """

    edge = self.get_edge(

        source,

        destination,

        edge_type,

    )

    if edge is None:

        return False

    edge.metadata.update(metadata)

    return True


###############################################################################


def get_edge(
    self,
    source: str,
    destination: str,
    edge_type: EdgeType,
) -> Optional[GraphEdge]:
    """
    Return graph edge.
    """

    if not self.graph.has_edge(

        source,

        destination,

    ):

        return None

    data = self.graph.get_edge_data(

        source,

        destination,

    )

    if edge_type.name not in data:

        return None

    return data[
        edge_type.name
    ]["data"]


###############################################################################


def edge_exists(
    self,
    source: str,
    destination: str,
    edge_type: Optional[EdgeType] = None,
) -> bool:
    """
    Check edge existence.
    """

    if edge_type is None:

        return self.graph.has_edge(

            source,

            destination,

        )

    return self.get_edge(

        source,

        destination,

        edge_type,

    ) is not None


###############################################################################


def funding_edge(
    self,
    source: str,
    destination: str,
    amount: float,
    metadata: Optional[Dict[str, Any]] = None,
) -> GraphEdge:
    """
    Create funding relationship.
    """

    metadata = metadata or {}

    metadata["amount"] = amount

    return self.add_edge(

        source,

        destination,

        EdgeType.FUNDING,

        weight=amount,

        metadata=metadata,

    )


###############################################################################


def transfer_edge(
    self,
    source: str,
    destination: str,
    amount: float,
    metadata: Optional[Dict[str, Any]] = None,
) -> GraphEdge:
    """
    Create transfer relationship.
    """

    metadata = metadata or {}

    metadata["amount"] = amount

    return self.add_edge(

        source,

        destination,

        EdgeType.TRANSFER,

        weight=amount,

        metadata=metadata,

    )


###############################################################################


def deployment_edge(
    self,
    deployer: str,
    token: str,
    metadata: Optional[Dict[str, Any]] = None,
) -> GraphEdge:
    """
    Create deployment relationship.
    """

    return self.add_edge(

        deployer,

        token,

        EdgeType.DEPLOYMENT,

        metadata=metadata,

    )


###############################################################################


def interaction_edge(
    self,
    wallet: str,
    target: str,
    metadata: Optional[Dict[str, Any]] = None,
) -> GraphEdge:
    """
    Create interaction relationship.
    """

    return self.add_edge(

        wallet,

        target,

        EdgeType.INTERACTION,

        metadata=metadata,

    )


###############################################################################


def bundle_edge(
    self,
    bundle: str,
    wallet: str,
    metadata: Optional[Dict[str, Any]] = None,
) -> GraphEdge:
    """
    Connect wallet to bundle.
    """

    return self.add_edge(

        bundle,

        wallet,

        EdgeType.BUNDLE,

        metadata=metadata,

    )

###############################################################################
# Graph Information
###############################################################################

def nodes(self) -> List[GraphNode]:
    """
    Return all graph nodes.

    Returns
    -------
    List[GraphNode]
    """

    return [

        data["data"]

        for _, data in self.graph.nodes(data=True)

    ]


###############################################################################


def edges(self) -> List[GraphEdge]:
    """
    Return all graph edges.

    Returns
    -------
    List[GraphEdge]
    """

    edge_list: List[GraphEdge] = []

    for _, _, _, data in self.graph.edges(

        keys=True,

        data=True,

    ):

        edge_list.append(

            data["data"]

        )

    return edge_list


###############################################################################


def wallets(self) -> List[GraphNode]:
    """
    Return all wallet nodes.

    Returns
    -------
    List[GraphNode]
    """

    return [

        self.get_node(wallet)

        for wallet in self.wallet_index

    ]


###############################################################################


def tokens(self) -> List[GraphNode]:
    """
    Return all token nodes.

    Returns
    -------
    List[GraphNode]
    """

    return [

        self.get_node(token)

        for token in self.token_index

    ]


###############################################################################


def deployers(self) -> List[GraphNode]:
    """
    Return all deployer nodes.

    Returns
    -------
    List[GraphNode]
    """

    return [

        self.get_node(deployer)

        for deployer in self.deployer_index

    ]


###############################################################################


def bundles(self) -> List[GraphNode]:
    """
    Return all bundle nodes.

    Returns
    -------
    List[GraphNode]
    """

    return [

        self.get_node(bundle)

        for bundle in self.bundle_index

    ]


###############################################################################


def wallet_count(self) -> int:
    """
    Total wallet nodes.
    """

    return len(

        self.wallet_index

    )


###############################################################################


def token_count(self) -> int:
    """
    Total token nodes.
    """

    return len(

        self.token_index

    )


###############################################################################


def graph_size(self) -> Dict[str, int]:
    """
    Return graph size information.

    Returns
    -------
    Dict[str, int]
    """

    return {

        "nodes":

            self.graph.number_of_nodes(),

        "edges":

            self.graph.number_of_edges(),

        "wallets":

            self.wallet_count(),

        "tokens":

            self.token_count(),

        "deployers":

            len(

                self.deployer_index

            ),

        "bundles":

            len(

                self.bundle_index

            ),

    }

###############################################################################
# Wallet Relationships
###############################################################################

def funding_tree(
    self,
    wallet: str,
    depth: Optional[int] = None,
) -> nx.MultiDiGraph:
    """
    Build funding tree for a wallet.

    Returns
    -------
    nx.MultiDiGraph
    """

    depth = depth or self.max_depth

    visited: Set[str] = set()

    queue: Deque[Tuple[str, int]] = deque()

    queue.append((wallet, 0))

    nodes: Set[str] = set()

    while queue:

        current, current_depth = queue.popleft()

        if current in visited:

            continue

        visited.add(current)

        nodes.add(current)

        if current_depth >= depth:

            continue

        for parent in self.predecessors(current):

            queue.append(

                (parent, current_depth + 1)

            )

    return self.subgraph(nodes)


###############################################################################


def wallet_relationships(
    self,
    wallet: str,
) -> Dict[str, List[str]]:
    """
    Return wallet relationship information.
    """

    return {

        "funders": self.predecessors(wallet),

        "receivers": self.successors(wallet),

        "neighbors": self.neighbors(wallet),

    }


###############################################################################


def common_funders(
    self,
    wallet_a: str,
    wallet_b: str,
) -> List[str]:
    """
    Return common funding wallets.
    """

    return list(

        set(self.predecessors(wallet_a))

        &

        set(self.predecessors(wallet_b))

    )


###############################################################################


def common_receivers(
    self,
    wallet_a: str,
    wallet_b: str,
) -> List[str]:
    """
    Return common receivers.
    """

    return list(

        set(self.successors(wallet_a))

        &

        set(self.successors(wallet_b))

    )


###############################################################################


def connected_wallets(
    self,
    wallet: str,
) -> Set[str]:
    """
    Return every connected wallet.
    """

    connected = set()

    connected.update(

        self.predecessors(wallet)

    )

    connected.update(

        self.successors(wallet)

    )

    connected.update(

        self.neighbors(wallet)

    )

    connected.discard(wallet)

    return connected


###############################################################################


def wallet_lineage(
    self,
    wallet: str,
) -> List[str]:
    """
    Funding lineage.

    Returns shortest upstream chain.
    """

    lineage: List[str] = []

    current = wallet

    visited = set()

    while True:

        parents = self.predecessors(current)

        if not parents:

            break

        parent = parents[0]

        if parent in visited:

            break

        visited.add(parent)

        lineage.append(parent)

        current = parent

    return lineage


###############################################################################


def wallet_clusters(
    self,
    wallet: str,
) -> Set[str]:
    """
    Return connected wallet cluster.
    """

    if wallet not in self.graph:

        return set()

    undirected = self.graph.to_undirected()

    for cluster in nx.connected_components(undirected):

        if wallet in cluster:

            return set(cluster)

    return set()


###############################################################################


def relationship_strength(
    self,
    wallet_a: str,
    wallet_b: str,
) -> float:
    """
    Compute simple relationship strength.

    Returns
    -------
    float
        0.0 -> no relationship
        1.0 -> identical relationship set
    """

    connections_a = self.connected_wallets(wallet_a)

    connections_b = self.connected_wallets(wallet_b)

    union = connections_a | connections_b

    if not union:

        return 0.0

    intersection = connections_a & connections_b

    return len(intersection) / len(union)

###############################################################################
# Token Relationships
###############################################################################

def token_holders(
    self,
    token: str,
) -> List[str]:
    """
    Return wallets connected to a token.

    Returns
    -------
    List[str]
    """

    if token not in self.graph:

        return []

    holders: Set[str] = set()

    holders.update(

        self.predecessors(token)

    )

    holders.update(

        self.successors(token)

    )

    return [

        wallet

        for wallet in holders

        if self.node_types.get(wallet) == NodeType.WALLET

    ]


###############################################################################


def token_deployer(
    self,
    token: str,
) -> Optional[str]:
    """
    Return deployer of a token.

    Returns
    -------
    Optional[str]
    """

    if token not in self.graph:

        return None

    for deployer in self.predecessors(token):

        edge = self.get_edge(

            deployer,

            token,

            EdgeType.DEPLOYMENT,

        )

        if edge is not None:

            return deployer

    return None


###############################################################################


def token_funding(
    self,
    token: str,
) -> List[str]:
    """
    Return funding wallets for a token.

    Returns
    -------
    List[str]
    """

    if token not in self.graph:

        return []

    funders: List[str] = []

    for wallet in self.predecessors(token):

        edge = self.get_edge(

            wallet,

            token,

            EdgeType.FUNDING,

        )

        if edge is not None:

            funders.append(wallet)

    return funders


###############################################################################


def token_clusters(
    self,
    token: str,
) -> Set[str]:
    """
    Return cluster containing token.

    Returns
    -------
    Set[str]
    """

    if token not in self.graph:

        return set()

    graph = self.graph.to_undirected()

    for cluster in nx.connected_components(graph):

        if token in cluster:

            return set(cluster)

    return set()


###############################################################################


def token_lineage(
    self,
    token: str,
) -> List[str]:
    """
    Return token ancestry.

    Returns
    -------
    List[str]
    """

    lineage: List[str] = []

    deployer = self.token_deployer(token)

    if deployer:

        lineage.append(deployer)

        lineage.extend(

            self.wallet_lineage(deployer)

        )

    return lineage


###############################################################################


def token_transfers(
    self,
    token: str,
) -> List[GraphEdge]:
    """
    Return transfer edges involving token.

    Returns
    -------
    List[GraphEdge]
    """

    transfers: List[GraphEdge] = []

    if token not in self.graph:

        return transfers

    for source, target, _, data in self.graph.edges(

        keys=True,

        data=True,

    ):

        edge: GraphEdge = data["data"]

        if (

            edge.edge_type == EdgeType.TRANSFER

            and

            (

                source == token

                or

                target == token

            )

        ):

            transfers.append(edge)

    return transfers


###############################################################################


def token_relationships(
    self,
    token: str,
) -> Dict[str, Any]:
    """
    Return complete token relationship summary.

    Returns
    -------
    Dict[str, Any]
    """

    return {

        "deployer":

            self.token_deployer(token),

        "holders":

            self.token_holders(token),

        "funders":

            self.token_funding(token),

        "cluster":

            list(

                self.token_clusters(token)

            ),

        "lineage":

            self.token_lineage(token),

        "transfers":

            len(

                self.token_transfers(token)

            ),

    }

###############################################################################
# Funding Graph
###############################################################################

def funding_sources(
    self,
    wallet: str,
) -> List[str]:
    """
    Return wallets funding the given wallet.

    Returns
    -------
    List[str]
    """

    if wallet not in self.graph:

        return []

    sources: List[str] = []

    for parent in self.predecessors(wallet):

        edge = self.get_edge(

            parent,

            wallet,

            EdgeType.FUNDING,

        )

        if edge is not None:

            sources.append(parent)

    return sources


###############################################################################


def funding_destinations(
    self,
    wallet: str,
) -> List[str]:
    """
    Return wallets funded by the given wallet.

    Returns
    -------
    List[str]
    """

    if wallet not in self.graph:

        return []

    destinations: List[str] = []

    for child in self.successors(wallet):

        edge = self.get_edge(

            wallet,

            child,

            EdgeType.FUNDING,

        )

        if edge is not None:

            destinations.append(child)

    return destinations


###############################################################################


def funding_depth(
    self,
    wallet: str,
) -> int:
    """
    Maximum upstream funding depth.

    Returns
    -------
    int
    """

    depth = 0

    current = wallet

    visited = set()

    while True:

        parents = self.funding_sources(current)

        if not parents:

            break

        parent = parents[0]

        if parent in visited:

            break

        visited.add(parent)

        current = parent

        depth += 1

    return depth


###############################################################################


def funding_chain(
    self,
    wallet: str,
) -> List[str]:
    """
    Return complete funding chain.

    Returns
    -------
    List[str]
    """

    chain: List[str] = []

    current = wallet

    visited = set()

    while True:

        parents = self.funding_sources(current)

        if not parents:

            break

        parent = parents[0]

        if parent in visited:

            break

        visited.add(parent)

        chain.append(parent)

        current = parent

    return chain


###############################################################################


def funding_subgraph(
    self,
    wallet: str,
    depth: Optional[int] = None,
) -> nx.MultiDiGraph:
    """
    Return funding subgraph.

    Returns
    -------
    nx.MultiDiGraph
    """

    return self.funding_tree(

        wallet,

        depth=depth,

    )


###############################################################################


def funding_roots(self) -> List[str]:
    """
    Return wallets with no funding source.

    Returns
    -------
    List[str]
    """

    roots: List[str] = []

    for wallet in self.wallet_index:

        if not self.funding_sources(wallet):

            roots.append(wallet)

    return roots


###############################################################################


def funding_leaves(self) -> List[str]:
    """
    Return wallets funding nobody else.

    Returns
    -------
    List[str]
    """

    leaves: List[str] = []

    for wallet in self.wallet_index:

        if not self.funding_destinations(wallet):

            leaves.append(wallet)

    return leaves


###############################################################################


def funding_statistics(self) -> Dict[str, Any]:
    """
    Funding graph statistics.

    Returns
    -------
    Dict[str, Any]
    """

    depths = [

        self.funding_depth(wallet)

        for wallet in self.wallet_index

    ]

    return {

        "wallets":

            self.wallet_count(),

        "roots":

            len(

                self.funding_roots()

            ),

        "leaves":

            len(

                self.funding_leaves()

            ),

        "average_depth":

            (

                sum(depths) / len(depths)

                if depths

                else 0.0

            ),

        "maximum_depth":

            (

                max(depths)

                if depths

                else 0

            ),

        "funding_edges":

            sum(

                1

                for _, _, _, data in self.graph.edges(

                    keys=True,

                    data=True,

                )

                if data["data"].edge_type == EdgeType.FUNDING

            ),

    }

###############################################################################
# Bundle Graph
###############################################################################

def bundle_members(
    self,
    bundle: str,
) -> List[str]:
    """
    Return all members of a bundle.

    Returns
    -------
    List[str]
    """

    if bundle not in self.graph:

        return []

    members: List[str] = []

    for node in self.successors(bundle):

        edge = self.get_edge(

            bundle,

            node,

            EdgeType.BUNDLE,

        )

        if edge is not None:

            members.append(node)

    return members


###############################################################################


def bundle_wallets(
    self,
    wallet: str,
) -> List[str]:
    """
    Return bundles containing a wallet.

    Returns
    -------
    List[str]
    """

    if wallet not in self.graph:

        return []

    bundles: List[str] = []

    for bundle in self.predecessors(wallet):

        edge = self.get_edge(

            bundle,

            wallet,

            EdgeType.BUNDLE,

        )

        if edge is not None:

            bundles.append(bundle)

    return bundles


###############################################################################


def bundle_size(
    self,
    bundle: str,
) -> int:
    """
    Number of members inside bundle.
    """

    return len(

        self.bundle_members(bundle)

    )


###############################################################################


def bundle_relationships(
    self,
    bundle: str,
) -> Dict[str, Any]:
    """
    Return bundle relationship summary.

    Returns
    -------
    Dict[str, Any]
    """

    members = self.bundle_members(bundle)

    return {

        "bundle": bundle,

        "members": members,

        "size": len(members),

    }


###############################################################################


def bundle_overlap(
    self,
    bundle_a: str,
    bundle_b: str,
) -> Dict[str, Any]:
    """
    Compare two bundles.

    Returns
    -------
    Dict[str, Any]
    """

    members_a = set(

        self.bundle_members(bundle_a)

    )

    members_b = set(

        self.bundle_members(bundle_b)

    )

    intersection = members_a & members_b

    union = members_a | members_b

    similarity = (

        len(intersection) / len(union)

        if union

        else 0.0

    )

    return {

        "shared_wallets": list(intersection),

        "shared_count": len(intersection),

        "similarity": similarity,

    }


###############################################################################


def bundle_subgraph(
    self,
    bundle: str,
) -> nx.MultiDiGraph:
    """
    Return subgraph containing bundle.

    Returns
    -------
    nx.MultiDiGraph
    """

    nodes = {

        bundle,

        *self.bundle_members(bundle),

    }

    return self.subgraph(nodes)


###############################################################################


def bundle_statistics(self) -> Dict[str, Any]:
    """
    Bundle graph statistics.

    Returns
    -------
    Dict[str, Any]
    """

    sizes = [

        self.bundle_size(bundle)

        for bundle in self.bundle_index

    ]

    return {

        "bundle_count":

            len(

                self.bundle_index

            ),

        "largest_bundle":

            max(sizes)

            if sizes

            else 0,

        "average_bundle_size":

            (

                sum(sizes) / len(sizes)

                if sizes

                else 0.0

            ),

        "bundle_edges":

            sum(

                1

                for _, _, _, data in self.graph.edges(

                    keys=True,

                    data=True,

                )

                if data["data"].edge_type == EdgeType.BUNDLE

            ),

    }

###############################################################################
# Deployer Graph
###############################################################################

def deployed_tokens(
    self,
    deployer: str,
) -> List[str]:
    """
    Return all tokens deployed by a deployer.

    Returns
    -------
    List[str]
    """

    if deployer not in self.graph:

        return []

    tokens: List[str] = []

    for token in self.successors(deployer):

        edge = self.get_edge(

            deployer,

            token,

            EdgeType.DEPLOYMENT,

        )

        if edge is not None:

            tokens.append(token)

    return tokens


###############################################################################


def deployer_wallets(
    self,
    deployer: str,
) -> List[str]:
    """
    Return wallets connected to the deployer.

    Returns
    -------
    List[str]
    """

    if deployer not in self.graph:

        return []

    wallets = set()

    wallets.update(

        self.predecessors(deployer)

    )

    wallets.update(

        self.successors(deployer)

    )

    return [

        wallet

        for wallet in wallets

        if self.node_types.get(wallet) == NodeType.WALLET

    ]


###############################################################################


def deployer_relationships(
    self,
    deployer: str,
) -> Dict[str, Any]:
    """
    Return deployer relationship summary.

    Returns
    -------
    Dict[str, Any]
    """

    return {

        "deployer":

            deployer,

        "tokens":

            self.deployed_tokens(deployer),

        "wallets":

            self.deployer_wallets(deployer),

        "launch_count":

            len(

                self.deployed_tokens(deployer)

            ),

    }


###############################################################################


def deployer_network(
    self,
    deployer: str,
) -> Set[str]:
    """
    Return all nodes connected to deployer.

    Returns
    -------
    Set[str]
    """

    if deployer not in self.graph:

        return set()

    graph = self.graph.to_undirected()

    return nx.node_connected_component(

        graph,

        deployer,

    )


###############################################################################


def deployer_clusters(
    self,
    deployer: str,
) -> Set[str]:
    """
    Return cluster containing deployer.

    Returns
    -------
    Set[str]
    """

    graph = self.graph.to_undirected()

    for cluster in nx.connected_components(graph):

        if deployer in cluster:

            return set(cluster)

    return set()


###############################################################################


def deployer_subgraph(
    self,
    deployer: str,
) -> nx.MultiDiGraph:
    """
    Return deployer subgraph.

    Returns
    -------
    nx.MultiDiGraph
    """

    nodes = {

        deployer,

        *self.deployed_tokens(deployer),

        *self.deployer_wallets(deployer),

    }

    return self.subgraph(nodes)


###############################################################################


def deployer_statistics(self) -> Dict[str, Any]:
    """
    Return deployer graph statistics.

    Returns
    -------
    Dict[str, Any]
    """

    launches = [

        len(

            self.deployed_tokens(

                deployer

            )

        )

        for deployer in self.deployer_index

    ]

    return {

        "deployer_count":

            len(

                self.deployer_index

            ),

        "token_launches":

            sum(launches),

        "average_launches":

            (

                sum(launches) / len(launches)

                if launches

                else 0.0

            ),

        "maximum_launches":

            max(launches)

            if launches

            else 0,

        "deployment_edges":

            sum(

                1

                for _, _, _, data in self.graph.edges(

                    keys=True,

                    data=True,

                )

                if data["data"].edge_type == EdgeType.DEPLOYMENT

            ),

    }

###############################################################################
# Graph Operations
###############################################################################

def merge(
    self,
    other: "WalletGraph",
) -> None:
    """
    Merge another WalletGraph into this graph.
    """

    if other is None:

        return

    # Merge graph structure
    self.graph = nx.compose(
        self.graph,
        other.graph,
    )

    # Merge indexes
    self.wallet_index.update(other.wallet_index)
    self.token_index.update(other.token_index)
    self.deployer_index.update(other.deployer_index)
    self.bundle_index.update(other.bundle_index)

    self.node_types.update(other.node_types)
    self.edge_types.update(other.edge_types)

    # Merge caches
    self.node_cache.update(other.node_cache)
    self.edge_cache.update(other.edge_cache)

    self.updated_at = time.time()


###############################################################################


def clone(self) -> "WalletGraph":
    """
    Create a deep copy of the graph.

    Returns
    -------
    WalletGraph
    """

    return copy.deepcopy(self)


###############################################################################


def clear(self) -> None:
    """
    Remove every node and edge while
    keeping configuration intact.
    """

    self.graph.clear()

    self.wallet_index.clear()
    self.token_index.clear()
    self.deployer_index.clear()
    self.bundle_index.clear()

    self.node_types.clear()
    self.edge_types.clear()

    self.node_cache.clear()
    self.edge_cache.clear()
    self.path_cache.clear()
    self.subgraph_cache.clear()
    self.statistics_cache.clear()

    self.updated_at = time.time()


###############################################################################


def reset(self) -> None:
    """
    Reset graph back to an empty state.
    """

    self.clear()

    self.state = GraphState.READY

    self.created_at = time.time()

    self.updated_at = self.created_at


###############################################################################


def copy_subgraph(
    self,
    nodes: Iterable[str],
) -> "WalletGraph":
    """
    Create a new WalletGraph from a
    subset of nodes.

    Returns
    -------
    WalletGraph
    """

    graph = self.clone()

    graph.graph = self.graph.subgraph(nodes).copy()

    return graph


###############################################################################


def remove_isolated(self) -> int:
    """
    Remove isolated nodes.

    Returns
    -------
    int
        Number of nodes removed.
    """

    isolated = list(
        nx.isolates(self.graph)
    )

    self.graph.remove_nodes_from(
        isolated
    )

    for node in isolated:

        self.wallet_index.pop(node, None)
        self.token_index.pop(node, None)
        self.deployer_index.pop(node, None)
        self.bundle_index.pop(node, None)

        self.node_types.pop(node, None)
        self.node_cache.pop(node, None)

    self.updated_at = time.time()

    return len(isolated)


###############################################################################


def simplify(self) -> None:
    """
    Remove duplicate parallel edges.

    Keeps one edge per
    (source, destination, edge type).
    """

    seen = set()

    duplicates = []

    for source, target, key in self.graph.edges(keys=True):

        identifier = (
            source,
            target,
            key,
        )

        if identifier in seen:

            duplicates.append(
                (source, target, key)
            )

        else:

            seen.add(identifier)

    for source, target, key in duplicates:

        self.graph.remove_edge(
            source,
            target,
            key=key,
        )

    self.updated_at = time.time()


###############################################################################


def optimize(self) -> Dict[str, Any]:
    """
    Perform lightweight graph optimization.

    Returns
    -------
    Dict[str, Any]
    """

    removed = self.remove_isolated()

    self.simplify()

    self.statistics_cache.clear()

    self.updated_at = time.time()

    return {

        "isolated_removed": removed,

        "nodes": self.graph.number_of_nodes(),

        "edges": self.graph.number_of_edges(),

        "optimized": True,

        "timestamp": self.updated_at,

    }

###############################################################################
# Search
###############################################################################

def search_wallet(
    self,
    wallet: str,
) -> Optional[GraphNode]:
    """
    Search for a wallet node by address.

    Parameters
    ----------
    wallet : str

    Returns
    -------
    Optional[GraphNode]
    """

    if wallet in self.wallet_index:

        return self.get_node(wallet)

    return None


###############################################################################


def search_token(
    self,
    token: str,
) -> Optional[GraphNode]:
    """
    Search for a token node.

    Parameters
    ----------
    token : str

    Returns
    -------
    Optional[GraphNode]
    """

    if token in self.token_index:

        return self.get_node(token)

    return None


###############################################################################


def search_deployer(
    self,
    deployer: str,
) -> Optional[GraphNode]:
    """
    Search for a deployer node.

    Parameters
    ----------
    deployer : str

    Returns
    -------
    Optional[GraphNode]
    """

    if deployer in self.deployer_index:

        return self.get_node(deployer)

    return None


###############################################################################


def search_bundle(
    self,
    bundle: str,
) -> Optional[GraphNode]:
    """
    Search for a bundle node.

    Parameters
    ----------
    bundle : str

    Returns
    -------
    Optional[GraphNode]
    """

    if bundle in self.bundle_index:

        return self.get_node(bundle)

    return None


###############################################################################


def find_path(
    self,
    source: str,
    destination: str,
) -> List[str]:
    """
    Find shortest path between two nodes.

    Parameters
    ----------
    source : str

    destination : str

    Returns
    -------
    List[str]
    """

    return self.shortest_path(

        source,

        destination,

    )


###############################################################################


def find_neighbors(
    self,
    node: str,
    depth: int = 1,
) -> Set[str]:
    """
    Find neighbors up to a given depth.

    Parameters
    ----------
    node : str

    depth : int

    Returns
    -------
    Set[str]
    """

    if node not in self.graph:

        return set()

    visited: Set[str] = set()

    queue: Deque[Tuple[str, int]] = deque()

    queue.append(

        (node, 0)

    )

    while queue:

        current, current_depth = queue.popleft()

        if current in visited:

            continue

        visited.add(current)

        if current_depth >= depth:

            continue

        for neighbor in self.neighbors(current):

            queue.append(

                (

                    neighbor,

                    current_depth + 1,

                )

            )

    visited.discard(node)

    return visited


###############################################################################


def query(
    self,
    keyword: str,
) -> Dict[str, List[GraphNode]]:
    """
    Perform generic graph search.

    Searches:

    - Wallets
    - Tokens
    - Deployers
    - Bundles

    Parameters
    ----------
    keyword : str

    Returns
    -------
    Dict[str, List[GraphNode]]
    """

    keyword = keyword.lower()

    results = {

        "wallets": [],

        "tokens": [],

        "deployers": [],

        "bundles": [],

    }

    ###########################################################################
    # Wallets
    ###########################################################################

    for wallet in self.wallet_index:

        if keyword in wallet.lower():

            node = self.get_node(wallet)

            if node:

                results["wallets"].append(node)

    ###########################################################################
    # Tokens
    ###########################################################################

    for token in self.token_index:

        if keyword in token.lower():

            node = self.get_node(token)

            if node:

                results["tokens"].append(node)

    ###########################################################################
    # Deployers
    ###########################################################################

    for deployer in self.deployer_index:

        if keyword in deployer.lower():

            node = self.get_node(deployer)

            if node:

                results["deployers"].append(node)

    ###########################################################################
    # Bundles
    ###########################################################################

    for bundle in self.bundle_index:

        if keyword in bundle.lower():

            node = self.get_node(bundle)

            if node:

                results["bundles"].append(node)

    return results           

###############################################################################
# Validation
###############################################################################

def validate_graph(
    self,
) -> bool:
    """
    Validate overall graph integrity.

    Returns
    -------
    bool
    """

    return (

        self.validate_nodes()

        and

        self.validate_edges()

    )


###############################################################################


def validate_nodes(
    self,
) -> bool:
    """
    Validate every graph node.

    Checks:
    --------
    • Node exists
    • GraphNode object exists
    • Node type is valid
    • Node cache consistency

    Returns
    -------
    bool
    """

    for node_id, attributes in self.graph.nodes(data=True):

        if "data" not in attributes:

            return False

        node = attributes["data"]

        if not isinstance(node, GraphNode):

            return False

        if node.node_type not in NodeType:

            return False

        if node.node_id != node_id:

            return False

    return True


###############################################################################


def validate_edges(
    self,
) -> bool:
    """
    Validate every graph edge.

    Checks:
    --------
    • GraphEdge object exists
    • Source exists
    • Destination exists
    • Edge type valid

    Returns
    -------
    bool
    """

    for source, destination, _, attributes in self.graph.edges(

        keys=True,

        data=True,

    ):

        if "data" not in attributes:

            return False

        edge = attributes["data"]

        if not isinstance(edge, GraphEdge):

            return False

        if source not in self.graph:

            return False

        if destination not in self.graph:

            return False

        if edge.edge_type not in EdgeType:

            return False

    return True


###############################################################################


def repair_graph(
    self,
) -> Dict[str, int]:
    """
    Repair common graph inconsistencies.

    Repairs:
    --------
    • Removes dangling cache entries
    • Removes invalid indexes
    • Removes isolated nodes
    • Rebuilds node cache

    Returns
    -------
    Dict[str, int]
    """

    repaired = {

        "cache_entries": 0,

        "indexes": 0,

        "isolated_nodes": 0,

    }

    ###########################################################################
    # Repair Cache
    ###########################################################################

    invalid_cache = [

        node

        for node in self.node_cache

        if node not in self.graph

    ]

    for node in invalid_cache:

        self.node_cache.pop(node, None)

        repaired["cache_entries"] += 1

    ###########################################################################
    # Repair Indexes
    ###########################################################################

    for index in (

        self.wallet_index,

        self.token_index,

        self.deployer_index,

        self.bundle_index,

    ):

        invalid = [

            key

            for key in index

            if key not in self.graph

        ]

        for key in invalid:

            index.pop(key, None)

            repaired["indexes"] += 1

    ###########################################################################
    # Remove Isolated Nodes
    ###########################################################################

    repaired["isolated_nodes"] = (

        self.remove_isolated()

    )

    ###########################################################################
    # Rebuild Cache
    ###########################################################################

    self.node_cache.clear()

    for node_id, data in self.graph.nodes(data=True):

        self.node_cache[node_id] = data["data"]

    return repaired


###############################################################################


def integrity_report(
    self,
) -> Dict[str, Any]:
    """
    Generate graph integrity report.

    Returns
    -------
    Dict[str, Any]
    """

    node_valid = self.validate_nodes()

    edge_valid = self.validate_edges()

    graph_valid = (

        node_valid

        and

        edge_valid

    )

    return {

        "graph_valid": graph_valid,

        "nodes_valid": node_valid,

        "edges_valid": edge_valid,

        "node_count": self.graph.number_of_nodes(),

        "edge_count": self.graph.number_of_edges(),

        "wallets": len(self.wallet_index),

        "tokens": len(self.token_index),

        "deployers": len(self.deployer_index),

        "bundles": len(self.bundle_index),

        "cached_nodes": len(self.node_cache),

        "cached_edges": len(self.edge_cache),

        "timestamp": time.time(),

    }

###############################################################################
# Export / Import
###############################################################################

def export_json(
    self,
    file_path: Union[str, Path],
    indent: int = 4,
) -> Path:
    """
    Export complete graph as JSON.

    Parameters
    ----------
    file_path : str | Path
    indent : int

    Returns
    -------
    Path
    """

    file_path = Path(file_path)

    data = {
        "graph": {
            "name": self.graph_name,
            "version": self.graph_version,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        },
        "nodes": [],
        "edges": [],
    }

    ###########################################################################
    # Nodes
    ###########################################################################

    for node_id, attrs in self.graph.nodes(data=True):

        node: GraphNode = attrs["data"]

        data["nodes"].append(
            {
                "id": node.node_id,
                "type": node.node_type.name,
                "label": node.label,
                "metadata": node.metadata,
                "created_at": node.created_at,
                "updated_at": node.updated_at,
            }
        )

    ###########################################################################
    # Edges
    ###########################################################################

    for source, target, key, attrs in self.graph.edges(
        keys=True,
        data=True,
    ):

        edge: GraphEdge = attrs["data"]

        data["edges"].append(
            {
                "source": edge.source,
                "destination": edge.destination,
                "type": edge.edge_type.name,
                "weight": edge.weight,
                "metadata": edge.metadata,
                "created_at": edge.created_at,
            }
        )

    with open(file_path, "w", encoding="utf-8") as fp:

        json.dump(
            data,
            fp,
            indent=indent,
        )

    return file_path


###############################################################################


def import_json(
    self,
    file_path: Union[str, Path],
) -> None:
    """
    Import graph from JSON.

    Parameters
    ----------
    file_path : str | Path
    """

    file_path = Path(file_path)

    with open(file_path, "r", encoding="utf-8") as fp:

        data = json.load(fp)

    self.clear()

    ###########################################################################
    # Nodes
    ###########################################################################

    for node in data["nodes"]:

        node_type = NodeType[node["type"]]

        graph_node = GraphNode(
            node_id=node["id"],
            node_type=node_type,
            label=node["label"],
            metadata=node["metadata"],
            created_at=node["created_at"],
            updated_at=node["updated_at"],
        )

        self.graph.add_node(
            graph_node.node_id,
            data=graph_node,
        )

        self.node_cache[graph_node.node_id] = graph_node
        self.node_types[graph_node.node_id] = node_type

        if node_type == NodeType.WALLET:
            self.wallet_index[graph_node.node_id] = graph_node.node_id

        elif node_type == NodeType.TOKEN:
            self.token_index[graph_node.node_id] = graph_node.node_id

        elif node_type == NodeType.DEPLOYER:
            self.deployer_index[graph_node.node_id] = graph_node.node_id

        elif node_type == NodeType.BUNDLE:
            self.bundle_index[graph_node.node_id] = graph_node.node_id

    ###########################################################################
    # Edges
    ###########################################################################

    for edge in data["edges"]:

        self.add_edge(
            source=edge["source"],
            destination=edge["destination"],
            edge_type=EdgeType[edge["type"]],
            weight=edge["weight"],
            metadata=edge["metadata"],
        )


###############################################################################


def export_graphml(
    self,
    file_path: Union[str, Path],
) -> Path:
    """
    Export graph as GraphML.

    Parameters
    ----------
    file_path : str | Path

    Returns
    -------
    Path
    """

    file_path = Path(file_path)

    graph = nx.DiGraph()

    ###########################################################################
    # Nodes
    ###########################################################################

    for node_id, attrs in self.graph.nodes(data=True):

        node: GraphNode = attrs["data"]

        graph.add_node(
            node_id,
            type=node.node_type.name,
            label=node.label,
        )

    ###########################################################################
    # Edges
    ###########################################################################

    for source, target, _, attrs in self.graph.edges(
        keys=True,
        data=True,
    ):

        edge: GraphEdge = attrs["data"]

        graph.add_edge(
            source,
            target,
            type=edge.edge_type.name,
            weight=edge.weight,
        )

    nx.write_graphml(
        graph,
        file_path,
    )

    return file_path


###############################################################################


def export_csv(
    self,
    directory: Union[str, Path],
) -> Path:
    """
    Export graph into CSV files.

    Creates:

    nodes.csv
    edges.csv

    Parameters
    ----------
    directory : str | Path

    Returns
    -------
    Path
    """

    directory = Path(directory)

    directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    ###########################################################################
    # Nodes
    ###########################################################################

    nodes_file = directory / "nodes.csv"

    with open(nodes_file, "w", newline="", encoding="utf-8") as fp:

        writer = csv.writer(fp)

        writer.writerow(
            [
                "id",
                "type",
                "label",
            ]
        )

        for node_id, attrs in self.graph.nodes(data=True):

            node: GraphNode = attrs["data"]

            writer.writerow(
                [
                    node.node_id,
                    node.node_type.name,
                    node.label,
                ]
            )

    ###########################################################################
    # Edges
    ###########################################################################

    edges_file = directory / "edges.csv"

    with open(edges_file, "w", newline="", encoding="utf-8") as fp:

        writer = csv.writer(fp)

        writer.writerow(
            [
                "source",
                "destination",
                "type",
                "weight",
            ]
        )

        for source, destination, _, attrs in self.graph.edges(
            keys=True,
            data=True,
        ):

            edge: GraphEdge = attrs["data"]

            writer.writerow(
                [
                    edge.source,
                    edge.destination,
                    edge.edge_type.name,
                    edge.weight,
                ]
            )

    return directory


###############################################################################


def snapshot(
    self,
) -> GraphSnapshot:
    """
    Create graph snapshot.

    Returns
    -------
    GraphSnapshot
    """

    return GraphSnapshot(
        node_count=self.graph.number_of_nodes(),
        edge_count=self.graph.number_of_edges(),
        metadata={
            "wallets": len(self.wallet_index),
            "tokens": len(self.token_index),
            "deployers": len(self.deployer_index),
            "bundles": len(self.bundle_index),
        },
    )                                             