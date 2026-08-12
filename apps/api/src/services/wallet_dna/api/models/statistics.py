###############################################################################
# Imports
###############################################################################

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict

###############################################################################
# Base Model
###############################################################################


class StatisticsBase(BaseModel):
    """
    Base statistics model.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )


###############################################################################
# GlobalStatistics
###############################################################################


class GlobalStatistics(StatisticsBase):
    total_wallets: int
    total_tokens: int
    total_graphs: int
    total_clusters: int
    total_deployers: int
    total_bundles: int
    analyzed_wallets: int
    analyzed_tokens: int
    updated_at: datetime


###############################################################################
# WalletStatistics
###############################################################################


class WalletStatistics(StatisticsBase):
    wallet_count: int
    active_wallets: int
    average_score: float
    average_balance: float
    average_transactions: float
    average_wallet_age: float
    updated_at: datetime


###############################################################################
# TokenStatistics
###############################################################################


class TokenStatistics(StatisticsBase):
    token_count: int
    active_tokens: int
    average_marketcap: float
    average_liquidity: float
    average_holders: int
    average_volume: float
    updated_at: datetime


###############################################################################
# GraphStatistics
###############################################################################


class GraphStatistics(StatisticsBase):
    node_count: int
    edge_count: int
    cluster_count: int
    graph_density: float
    connected_components: int
    updated_at: datetime


###############################################################################
# FundingStatistics
###############################################################################


class FundingStatistics(StatisticsBase):
    funding_chains: int
    funding_nodes: int
    funding_edges: int
    suspicious_chains: int
    average_depth: float
    updated_at: datetime


###############################################################################
# RuntimeStatistics
###############################################################################


class RuntimeStatistics(StatisticsBase):
    uptime_seconds: float
    cpu_usage: float
    memory_usage: float
    websocket_connections: int
    worker_count: int
    request_count: int
    updated_at: datetime


###############################################################################
# DashboardMetrics
###############################################################################


class DashboardMetrics(StatisticsBase):
    wallets_online: int
    tokens_online: int
    alerts_today: int
    ai_requests: int
    graph_updates: int
    funding_events: int
    runtime_health: str
    updated_at: datetime


###############################################################################
# Utilities
###############################################################################


def statistics_summary(
    stats: StatisticsBase,
) -> dict[str, Any]:
    """
    Serialize statistics.
    """

    return stats.model_dump()


###############################################################################


def build_statistics_response(
    stats: StatisticsBase,
) -> dict[str, Any]:
    """
    Standard statistics response.
    """

    return {
        "success": True,
        "data": stats.model_dump(),
    }