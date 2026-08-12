from datetime import UTC, datetime, timedelta
from pathlib import Path
from time import monotonic, perf_counter
from uuid import UUID, uuid4

import asyncio
import hashlib
import itertools
import json
import logging
import math
import os


from datetime import (
    UTC,
    datetime,
    timedelta,
    timezone,
)

from pathlib import Path

from time import (
    perf_counter,
    monotonic,
)

from uuid import (
    UUID,
    uuid4,
)

# ============================================================================
# Typing
# ============================================================================

from typing import (
    Any,
    Callable,
    Dict,
    Generator,
    Iterable,
    Iterator,
    List,
    Optional,
    Sequence,
    Set,
    Tuple,
    Union,
)

from collections.abc import (
    Callable,
    Generator,
    Iterable,
    Iterator,
    Sequence,
)

from typing import (
    Any,
    Optional,
)

dict[str, Any]
list[str]
set[str]
tuple[int, str]

# ============================================================================
# Dataclasses
# ============================================================================

from dataclasses import (
    asdict,
    astuple,
    dataclass,
    field,
    fields,
    replace,
)

# ============================================================================
# Collections
# ============================================================================

from collections import (
    ChainMap,
    Counter,
    defaultdict,
    deque,
)

# ============================================================================
# Third-Party Libraries
# ============================================================================

import aiofiles
import cachetools
import networkx as nx
import numpy as np
import orjson
import rustworkx as rx

from cachetools import (
    Cache,
    FIFOCache,
    LFUCache,
    LRUCache,
    TTLCache,
    cached,
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationError,
    field_validator,
    model_validator,
)

# ============================================================================
# Internal Modules
# ============================================================================

# Database
from sentinel_ai.database.wallet_database import WalletDatabase
from sentinel_ai.database.token_database import TokenDatabase

# Graph Engine
from sentinel_ai.graph.funding_graph_builder import FundingGraphBuilder

# Blockchain
from sentinel_ai.blockchain.transaction_fetcher import TransactionFetcher

# Cache
from sentinel_ai.cache.cache_manager import CacheManager

# Configuration
from sentinel_ai.config.config import Config

# Logging
from sentinel_ai.utils.logger import get_logger

# Models
from sentinel_ai.models.deployer_models import (
    DeployerConfig,
    DeployerGraphModel,
    DeployerNode,
    DeployerStatistics,
    LaunchHistory,
)

from sentinel_ai.models.wallet_models import (
    WalletNode,
    WalletRecord,
)

from sentinel_ai.models.transaction_models import (
    TransactionRecord,
    TransferRecord,
)

from sentinel_ai.models.token_models import (
    TokenRecord,
)

# ============================================================================
# Constants
# ============================================================================

# Graph Version
GRAPH_VERSION: str = "1.0.0"

# Unknown Values
UNKNOWN_DEPLOYER: str = "UNKNOWN_DEPLOYER"

# Graph Limits
MAX_GRAPH_DEPTH: int = 10
MAX_FUNDING_DEPTH: int = 6
MAX_RELATED_WALLETS: int = 1000
MAX_TOKEN_HISTORY: int = 500
MAX_CLUSTER_SIZE: int = 10000

# Analysis Defaults
DEFAULT_LOOKBACK_DAYS: int = 365
DEFAULT_BATCH_SIZE: int = 500
DEFAULT_TIMEOUT: float = 30.0

# Cache
DEFAULT_CACHE_TTL: int = 300  # seconds

# Edge Weights
MIN_EDGE_WEIGHT: float = 0.0
MAX_EDGE_WEIGHT: float = 1.0

# Risk Thresholds
LOW_RISK_THRESHOLD: float = 0.25
MEDIUM_RISK_THRESHOLD: float = 0.50
HIGH_RISK_THRESHOLD: float = 0.75
CRITICAL_RISK_THRESHOLD: float = 0.90

# Reputation Thresholds
GOOD_REPUTATION_SCORE: float = 80.0
WARNING_REPUTATION_SCORE: float = 50.0
BAD_REPUTATION_SCORE: float = 20.0

# Graph Analytics
MAX_PATH_LENGTH: int = 25
MAX_NEIGHBOR_SCAN: int = 10000
MAX_GRAPH_ITERATIONS: int = 100000

# Funding Analysis
MIN_FUNDING_AMOUNT_SOL: float = 0.01
MIN_EDGE_CONFIDENCE: float = 0.50

# Performance
DEFAULT_WORKERS: int = 8
MAX_CONCURRENT_TASKS: int = 64

# Serialization
DEFAULT_ENCODING: str = "utf-8"

# Export
DEFAULT_EXPORT_FORMAT: str = "json"

# ============================================================================
# Enums
# ============================================================================

from enum import Enum


class DeployerRisk(str, Enum):
    UNKNOWN = "unknown"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class FundingSource(str, Enum):
    UNKNOWN = "unknown"
    BINANCE = "binance"
    BYBIT = "bybit"
    OKX = "okx"
    COINBASE = "coinbase"
    KRAKEN = "kraken"
    KUCOIN = "kucoin"
    MEXC = "mexc"
    GATE = "gate"
    PERSONAL_WALLET = "personal_wallet"
    MIXER = "mixer"
    BRIDGE = "bridge"
    OTHER = "other"


class WalletRelationType(str, Enum):
    FUNDER = "funder"
    FUNDED = "funded"
    DEPLOYER = "deployer"
    TEAM = "team"
    INSIDER = "insider"
    SNIPER = "sniper"
    HOLDER = "holder"
    EXCHANGE = "exchange"
    UNKNOWN = "unknown"


class LaunchStatus(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    SUCCESS = "success"
    FAILED = "failed"
    RUGGED = "rugged"
    ABANDONED = "abandoned"


class ReputationLevel(str, Enum):
    UNKNOWN = "unknown"
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    DANGEROUS = "dangerous"


class GraphState(str, Enum):
    EMPTY = "empty"
    BUILDING = "building"
    READY = "ready"
    UPDATING = "updating"
    STALE = "stale"
    FAILED = "failed"


class NodeType(str, Enum):
    DEPLOYER = "deployer"
    WALLET = "wallet"
    TOKEN = "token"
    EXCHANGE = "exchange"
    PROGRAM = "program"
    UNKNOWN = "unknown"


class EdgeType(str, Enum):
    FUNDING = "funding"
    DEPLOYMENT = "deployment"
    OWNERSHIP = "ownership"
    TRANSFER = "transfer"
    TOKEN_FLOW = "token_flow"
    RELATIONSHIP = "relationship"


class AnalysisMode(str, Enum):
    QUICK = "quick"
    STANDARD = "standard"
    DEEP = "deep"
    FORENSIC = "forensic"