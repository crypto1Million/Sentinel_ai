###############################################################################
# Standard Library
###############################################################################

from __future__ import annotations

import asyncio
import contextlib
import logging
import os
from functools import lru_cache
from pathlib import Path
from typing import Any, AsyncGenerator

###############################################################################
# FastAPI
###############################################################################

from fastapi import Depends

###############################################################################
# API Configuration
###############################################################################

from wallet_dna.api.config import APIConfig

###############################################################################
# Storage
###############################################################################

from wallet_dna.storage.postgresql import PostgreSQL
from wallet_dna.storage.redis_client import RedisClient
from wallet_dna.storage.clickhouse_client import ClickHouseClient
from wallet_dna.storage.neo4j_client import Neo4jClient

###############################################################################
# Blockchain Clients
###############################################################################

from wallet_dna.clients.helius_client import HeliusClient
from wallet_dna.clients.rpc_client import RPCClient
from wallet_dna.clients.jupiter_client import JupiterClient
from wallet_dna.clients.raydium_client import RaydiumClient
from wallet_dna.clients.pumpfun_client import PumpFunClient
from wallet_dna.clients.dexscreener_client import DexScreenerClient
from wallet_dna.clients.birdeye_client import BirdeyeClient

###############################################################################
# Graph
###############################################################################

from wallet_dna.graph.wallet_graph import WalletGraph
from wallet_dna.graph.graph_cache import GraphCache
from wallet_dna.graph.graph_runtime import GraphRuntime
from wallet_dna.graph.graph_statistics import GraphStatistics

###############################################################################
# Validators
###############################################################################

from wallet_dna.validators.wallet_validator import WalletValidator
from wallet_dna.validators.token_validator import TokenValidator
from wallet_dna.validators.transaction_validator import TransactionValidator
from wallet_dna.validators.graph_validator import GraphValidator

###############################################################################
# AI
###############################################################################

from wallet_dna.ai.wallet_dna_analyzer import WalletDNAAnalyzer
from wallet_dna.ai.cluster_analyzer import ClusterAnalyzer
from wallet_dna.ai.funding_analyzer import FundingAnalyzer
from wallet_dna.ai.deployer_analyzer import DeployerAnalyzer
from wallet_dna.ai.risk_analyzer import RiskAnalyzer

###############################################################################
# Runtime
###############################################################################

from wallet_dna.runtime.event_bus import EventBus
from wallet_dna.runtime.metrics import MetricsCollector
from wallet_dna.runtime.progress import ProgressTracker
from wallet_dna.runtime.rate_limiter import RateLimiter

###############################################################################
# Security
###############################################################################

from wallet_dna.api.security import (
    get_current_user,
    verify_api_key,
)

###############################################################################
# Configuration
###############################################################################

@lru_cache(maxsize=1)
def get_config() -> APIConfig:
    """
    Return the singleton API configuration.

    Returns
    -------
    APIConfig
    """

    return APIConfig()

###############################################################################
# Database Dependencies
###############################################################################

@lru_cache(maxsize=1)
def get_postgres() -> PostgreSQL:
    """
    Return the shared PostgreSQL client.

    Returns
    -------
    PostgreSQL
    """

    config = get_config()

    return PostgreSQL(

        host=config.POSTGRES_HOST,

        port=config.POSTGRES_PORT,

        database=config.POSTGRES_DATABASE,

        username=config.POSTGRES_USER,

        password=config.POSTGRES_PASSWORD,

    )


###############################################################################


@lru_cache(maxsize=1)
def get_clickhouse() -> ClickHouseClient:
    """
    Return the shared ClickHouse client.

    Returns
    -------
    ClickHouseClient
    """

    config = get_config()

    return ClickHouseClient(

        host=config.CLICKHOUSE_HOST,

        port=config.CLICKHOUSE_PORT,

        database=config.CLICKHOUSE_DATABASE,

        username=config.CLICKHOUSE_USER,

        password=config.CLICKHOUSE_PASSWORD,

    )


###############################################################################


@lru_cache(maxsize=1)
def get_neo4j() -> Neo4jClient:
    """
    Return the shared Neo4j client.

    Returns
    -------
    Neo4jClient
    """

    config = get_config()

    return Neo4jClient(

        uri=config.NEO4J_URI,

        username=config.NEO4J_USER,

        password=config.NEO4J_PASSWORD,

    )


###############################################################################


@lru_cache(maxsize=1)
def get_redis() -> RedisClient:
    """
    Return the shared Redis client.

    Returns
    -------
    RedisClient
    """

    config = get_config()

    return RedisClient(

        host=config.REDIS_HOST,

        port=config.REDIS_PORT,

        password=config.REDIS_PASSWORD,

        db=config.REDIS_DATABASE,

    )

###############################################################################
# Blockchain Client Dependencies
###############################################################################

@lru_cache(maxsize=1)
def get_helius() -> HeliusClient:
    """
    Return the shared Helius client.

    Returns
    -------
    HeliusClient
    """

    config = get_config()

    return HeliusClient(

        api_key=config.HELIUS_API_KEY,

        base_url=config.HELIUS_BASE_URL,

        timeout=config.CLIENT_TIMEOUT,

    )


###############################################################################


@lru_cache(maxsize=1)
def get_rpc() -> RPCClient:
    """
    Return the shared Solana RPC client.

    Returns
    -------
    RPCClient
    """

    config = get_config()

    return RPCClient(

        rpc_url=config.SOLANA_RPC_URL,

        timeout=config.CLIENT_TIMEOUT,

    )


###############################################################################


@lru_cache(maxsize=1)
def get_jupiter() -> JupiterClient:
    """
    Return the shared Jupiter client.

    Returns
    -------
    JupiterClient
    """

    config = get_config()

    return JupiterClient(

        base_url=config.JUPITER_API_URL,

        timeout=config.CLIENT_TIMEOUT,

    )


###############################################################################


@lru_cache(maxsize=1)
def get_raydium() -> RaydiumClient:
    """
    Return the shared Raydium client.

    Returns
    -------
    RaydiumClient
    """

    config = get_config()

    return RaydiumClient(

        base_url=config.RAYDIUM_API_URL,

        timeout=config.CLIENT_TIMEOUT,

    )


###############################################################################


@lru_cache(maxsize=1)
def get_pumpfun() -> PumpFunClient:
    """
    Return the shared Pump.fun client.

    Returns
    -------
    PumpFunClient
    """

    config = get_config()

    return PumpFunClient(

        base_url=config.PUMPFUN_API_URL,

        timeout=config.CLIENT_TIMEOUT,

    )


###############################################################################


@lru_cache(maxsize=1)
def get_dexscreener() -> DexScreenerClient:
    """
    Return the shared DexScreener client.

    Returns
    -------
    DexScreenerClient
    """

    config = get_config()

    return DexScreenerClient(

        base_url=config.DEXSCREENER_API_URL,

        timeout=config.CLIENT_TIMEOUT,

    )


###############################################################################


@lru_cache(maxsize=1)
def get_birdeye() -> BirdeyeClient:
    """
    Return the shared Birdeye client.

    Returns
    -------
    BirdeyeClient
    """

    config = get_config()

    return BirdeyeClient(

        api_key=config.BIRDEYE_API_KEY,

        base_url=config.BIRDEYE_API_URL,

        timeout=config.CLIENT_TIMEOUT,

    )

###############################################################################
# Graph Dependencies
###############################################################################

@lru_cache(maxsize=1)
def get_graph() -> WalletGraph:
    """
    Return the shared WalletGraph instance.

    Returns
    -------
    WalletGraph
    """

    config = get_config()

    return WalletGraph(

        config=config,

        postgres=get_postgres(),

        clickhouse=get_clickhouse(),

        neo4j=get_neo4j(),

        redis=get_redis(),

    )


###############################################################################


@lru_cache(maxsize=1)
def get_graph_cache() -> GraphCache:
    """
    Return the shared GraphCache instance.

    Returns
    -------
    GraphCache
    """

    config = get_config()

    return GraphCache(

        redis=get_redis(),

        config=config,

    )


###############################################################################


@lru_cache(maxsize=1)
def get_graph_runtime() -> GraphRuntime:
    """
    Return the shared GraphRuntime instance.

    Returns
    -------
    GraphRuntime
    """

    config = get_config()

    return GraphRuntime(

        graph=get_graph(),

        cache=get_graph_cache(),

        config=config,

    )


###############################################################################


@lru_cache(maxsize=1)
def get_graph_statistics() -> GraphStatistics:
    """
    Return the shared GraphStatistics instance.

    Returns
    -------
    GraphStatistics
    """

    config = get_config()

    return GraphStatistics(

        graph=get_graph(),

        cache=get_graph_cache(),

        runtime=get_graph_runtime(),

        config=config,

    )

###############################################################################
# Graph Dependencies
###############################################################################

@lru_cache(maxsize=1)
def get_graph() -> WalletGraph:
    """
    Return the shared WalletGraph instance.

    Returns
    -------
    WalletGraph
    """

    config = get_config()

    return WalletGraph(

        config=config,

        postgres=get_postgres(),

        clickhouse=get_clickhouse(),

        neo4j=get_neo4j(),

        redis=get_redis(),

    )


###############################################################################


@lru_cache(maxsize=1)
def get_graph_cache() -> GraphCache:
    """
    Return the shared GraphCache instance.

    Returns
    -------
    GraphCache
    """

    config = get_config()

    return GraphCache(

        redis=get_redis(),

        config=config,

    )


###############################################################################


@lru_cache(maxsize=1)
def get_graph_runtime() -> GraphRuntime:
    """
    Return the shared GraphRuntime instance.

    Returns
    -------
    GraphRuntime
    """

    config = get_config()

    return GraphRuntime(

        graph=get_graph(),

        cache=get_graph_cache(),

        config=config,

    )


###############################################################################


@lru_cache(maxsize=1)
def get_graph_statistics() -> GraphStatistics:
    """
    Return the shared GraphStatistics instance.

    Returns
    -------
    GraphStatistics
    """

    config = get_config()

    return GraphStatistics(

        graph=get_graph(),

        cache=get_graph_cache(),

        runtime=get_graph_runtime(),

        config=config,

    )                

###############################################################################
# AI Dependencies
###############################################################################

@lru_cache(maxsize=1)
def get_wallet_dna() -> WalletDNAAnalyzer:
    """
    Return the shared Wallet DNA analyzer.

    Returns
    -------
    WalletDNAAnalyzer
    """

    return WalletDNAAnalyzer(

        graph=get_graph(),

        cache=get_graph_cache(),

        runtime=get_graph_runtime(),

        statistics=get_graph_statistics(),

        config=get_config(),

    )


###############################################################################


@lru_cache(maxsize=1)
def get_cluster_analyzer() -> ClusterAnalyzer:
    """
    Return the shared Cluster Analyzer.

    Returns
    -------
    ClusterAnalyzer
    """

    return ClusterAnalyzer(

        graph=get_graph(),

        wallet_dna=get_wallet_dna(),

        config=get_config(),

    )


###############################################################################


@lru_cache(maxsize=1)
def get_risk_analyzer() -> RiskAnalyzer:
    """
    Return the shared Risk Analyzer.

    Returns
    -------
    RiskAnalyzer
    """

    return RiskAnalyzer(

        graph=get_graph(),

        wallet_dna=get_wallet_dna(),

        cluster_analyzer=get_cluster_analyzer(),

        config=get_config(),

    )


###############################################################################


@lru_cache(maxsize=1)
def get_funding_analyzer() -> FundingAnalyzer:
    """
    Return the shared Funding Analyzer.

    Returns
    -------
    FundingAnalyzer
    """

    return FundingAnalyzer(

        graph=get_graph(),

        cache=get_graph_cache(),

        runtime=get_graph_runtime(),

        config=get_config(),

    )


###############################################################################


@lru_cache(maxsize=1)
def get_deployer_analyzer() -> DeployerAnalyzer:
    """
    Return the shared Deployer Analyzer.

    Returns
    -------
    DeployerAnalyzer
    """

    return DeployerAnalyzer(

        graph=get_graph(),

        funding_analyzer=get_funding_analyzer(),

        wallet_dna=get_wallet_dna(),

        config=get_config(),

    )

###############################################################################
# Runtime Dependencies
###############################################################################

@lru_cache(maxsize=1)
def get_event_bus() -> EventBus:
    """
    Return the shared Event Bus.

    Returns
    -------
    EventBus
    """

    return EventBus(

        redis=get_redis(),

        config=get_config(),

    )


###############################################################################


@lru_cache(maxsize=1)
def get_metrics() -> MetricsCollector:
    """
    Return the shared Metrics Collector.

    Returns
    -------
    MetricsCollector
    """

    return MetricsCollector(

        graph=get_graph(),

        runtime=get_graph_runtime(),

        redis=get_redis(),

        config=get_config(),

    )


###############################################################################


@lru_cache(maxsize=1)
def get_progress_tracker() -> ProgressTracker:
    """
    Return the shared Progress Tracker.

    Returns
    -------
    ProgressTracker
    """

    return ProgressTracker(

        redis=get_redis(),

        event_bus=get_event_bus(),

        config=get_config(),

    )


###############################################################################


@lru_cache(maxsize=1)
def get_rate_limiter() -> RateLimiter:
    """
    Return the shared API Rate Limiter.

    Returns
    -------
    RateLimiter
    """

    return RateLimiter(

        redis=get_redis(),

        metrics=get_metrics(),

        config=get_config(),

    )

###############################################################################
# Authentication Dependencies
###############################################################################

from fastapi import (
    Depends,
    Header,
    HTTPException,
    status,
)

from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

###############################################################################

bearer_scheme = HTTPBearer(auto_error=False)

###############################################################################


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        bearer_scheme
    ),
) -> dict:
    """
    Return authenticated user.

    Raises
    ------
    HTTPException
    """

    if credentials is None:

        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="Authentication required",

        )

    token = credentials.credentials

    user = verify_jwt(token)

    if user is None:

        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="Invalid JWT token",

        )

    return user


###############################################################################


async def get_current_wallet(
    user: dict = Depends(
        get_current_user
    ),
) -> str:
    """
    Return authenticated wallet.

    Returns
    -------
    str
    """

    wallet = user.get("wallet")

    if wallet is None:

        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="Wallet not linked",

        )

    return wallet


###############################################################################


async def require_admin(
    user: dict = Depends(
        get_current_user
    ),
) -> dict:
    """
    Require administrator access.
    """

    if not user.get("is_admin", False):

        raise HTTPException(

            status_code=status.HTTP_403_FORBIDDEN,

            detail="Administrator permission required",

        )

    return user


###############################################################################


async def verify_api_key(
    x_api_key: str | None = Header(
        default=None,
        alias="X-API-Key",
    ),
) -> str:
    """
    Verify API Key.
    """

    config = get_config()

    if x_api_key != config.API_KEY:

        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="Invalid API Key",

        )

    return x_api_key        


###############################################################################
# Pagination Dependencies
###############################################################################

from fastapi import Query

###############################################################################


def get_pagination(
    page: int = Query(
        default=1,
        ge=1,
        description="Page number",
    ),
    page_size: int = Query(
        default=50,
        ge=1,
        le=500,
        description="Items per page",
    ),
) -> dict:
    """
    Return pagination parameters.

    Returns
    -------
    dict
    """

    offset = (page - 1) * page_size

    return {

        "page": page,

        "page_size": page_size,

        "offset": offset,

        "limit": page_size,

    }


###############################################################################


def get_sorting(
    sort_by: str = Query(
        default="created_at",
        description="Sort field",
    ),
    order: str = Query(
        default="desc",
        pattern="^(asc|desc)$",
        description="Sort order",
    ),
) -> dict:
    """
    Return sorting parameters.

    Returns
    -------
    dict
    """

    return {

        "sort_by": sort_by,

        "order": order.lower(),

    }

###############################################################################
# Cleanup Dependencies
###############################################################################

async def startup_dependencies() -> None:
    """
    Initialize all shared services during API startup.

    Initializes
    -----------
    • PostgreSQL
    • Redis
    • ClickHouse
    • Neo4j
    • Helius
    • RPC
    • WalletGraph
    • Event Bus
    • Metrics
    """

    logging.info("Initializing Wallet DNA dependencies...")

    get_postgres().connect()

    get_clickhouse().connect()

    get_neo4j().connect()

    get_redis().connect()

    await get_helius().connect()

    await get_rpc().connect()

    get_graph()

    get_graph_cache()

    get_graph_runtime()

    get_graph_statistics()

    get_event_bus()

    get_metrics()

    get_progress_tracker()

    get_rate_limiter()

    logging.info("Wallet DNA dependencies initialized.")


###############################################################################


async def shutdown_dependencies() -> None:
    """
    Gracefully shutdown all shared services.

    Closes
    -------
    • PostgreSQL
    • Redis
    • ClickHouse
    • Neo4j
    • Helius
    • RPC
    • Event Bus
    """

    logging.info("Shutting down Wallet DNA dependencies...")

    with contextlib.suppress(Exception):
        get_postgres().disconnect()

    with contextlib.suppress(Exception):
        get_clickhouse().disconnect()

    with contextlib.suppress(Exception):
        get_neo4j().disconnect()

    with contextlib.suppress(Exception):
        get_redis().disconnect()

    with contextlib.suppress(Exception):
        await get_helius().disconnect()

    with contextlib.suppress(Exception):
        await get_rpc().disconnect()

    with contextlib.suppress(Exception):
        await get_event_bus().shutdown()

    logging.info("Wallet DNA dependencies shut down successfully.")    