from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Dict, List, Optional, Set

class WalletRole(str, Enum):
    UNKNOWN = "unknown"
    DEPLOYER = "deployer"
    SNIPER = "sniper"
    INSIDER = "insider"
    DEV = "dev"
    BUNDLER = "bundler"
    MARKET_MAKER = "market_maker"
    LP_PROVIDER = "lp_provider"
    HOLDER = "holder"


class EdgeType(str, Enum):
    FUNDING = "funding"
    DEPLOYMENT = "deployment"
    TRANSFER = "transfer"
    INTERACTION = "interaction"
    BUNDLE = "bundle"


class InteractionType(str, Enum):
    BUY = "buy"
    SELL = "sell"
    SWAP = "swap"
    MINT = "mint"
    BURN = "burn"
    ADD_LIQUIDITY = "add_liquidity"
    REMOVE_LIQUIDITY = "remove_liquidity"


@dataclass
class NodeMetrics:

    total_volume: Decimal = Decimal("0")

    buys: int = 0

    sells: int = 0

    pnl: Decimal = Decimal("0")

    win_rate: float = 0.0

    average_hold_time: float = 0.0

    rugs_created: int = 0

    rugs_bought: int = 0

    rugged_tokens: int = 0

    deployed_tokens: int = 0

    funded_wallets: int = 0

    incoming_edges: int = 0

    outgoing_edges: int = 0

    centrality: float = 0.0

    wallet_score: float = 0.0

    risk_score: float = 0.0

@dataclass
class WalletNode:

    address: str

    role: WalletRole = WalletRole.UNKNOWN

    first_seen: Optional[datetime] = None

    last_seen: Optional[datetime] = None

    metrics: NodeMetrics = field(default_factory=NodeMetrics)

    deployed_tokens: Set[str] = field(default_factory=set)

    holdings: Dict[str, Decimal] = field(default_factory=dict)

    labels: Set[str] = field(default_factory=set)

    metadata: Dict[str, str] = field(default_factory=dict)

@dataclass
class TokenNode:

    mint: str

    symbol: str = ""

    name: str = ""

    deployer: Optional[str] = None

    launch_time: Optional[datetime] = None

    market_cap: Decimal = Decimal("0")

    liquidity: Decimal = Decimal("0")

    holders: int = 0

    metadata: Dict[str, str] = field(default_factory=dict)

@dataclass
class GraphEdge:

    source: str

    target: str

    edge_type: EdgeType

    timestamp: Optional[datetime] = None

@dataclass
class FundingEdge(GraphEdge):

    amount: Decimal = Decimal("0")

    token: str = "SOL"

    tx_hash: Optional[str] = None

@dataclass
class DeploymentEdge(GraphEdge):

    token_mint: str = ""

    initial_supply: Decimal = Decimal("0")

    tx_hash: Optional[str] = None

@dataclass
class TransferEdge(GraphEdge):

    amount: Decimal = Decimal("0")

    token: str = ""

    tx_hash: Optional[str] = None

@dataclass
class BundleEdge(GraphEdge):

    bundle_id: str = ""

    wallets: List[str] = field(default_factory=list)

    coordinated: bool = False

@dataclass
class InteractionEdge(GraphEdge):

    interaction: InteractionType = InteractionType.BUY

    token: str = ""

    amount: Decimal = Decimal("0")

    tx_hash: Optional[str] = None

@dataclass
class GraphState:

    wallets: Dict[str, WalletNode] = field(default_factory=dict)

    tokens: Dict[str, TokenNode] = field(default_factory=dict)

    edges: List[GraphEdge] = field(default_factory=list)                                    