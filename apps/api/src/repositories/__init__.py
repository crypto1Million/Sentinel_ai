###############################################################################
# Imports
###############################################################################

from .base_repository import BaseRepository
from .session import DatabaseSession
from .transaction import TransactionManager

from .postgres_repository import PostgreSQLRepository
from .clickhouse_repository import ClickHouseRepository
from .neo4j_repository import Neo4jRepository
from .redis_repository import RedisRepository

from .wallet_repository import WalletRepository
from .token_repository import TokenRepository
from .funding_repository import FundingRepository
from .bundle_repository import BundleRepository
from .deployer_repository import DeployerRepository
from .cluster_repository import ClusterRepository
from .graph_repository import GraphRepository
from .wallet_dna_repository import WalletDNARepository
from .statistics_repository import StatisticsRepository
from .search_repository import SearchRepository
from .export_repository import ExportRepository

###############################################################################
# Version
###############################################################################

__version__ = "1.0.0"
__author__ = "Sentinel AI"

###############################################################################
# Repository Exports
###############################################################################

__all__ = [
    "BaseRepository",
    "DatabaseSession",
    "TransactionManager",

    "PostgreSQLRepository",
    "ClickHouseRepository",
    "Neo4jRepository",
    "RedisRepository",

    "WalletRepository",
    "TokenRepository",
    "FundingRepository",
    "BundleRepository",
    "DeployerRepository",
    "ClusterRepository",
    "GraphRepository",
    "WalletDNARepository",
    "StatisticsRepository",
    "SearchRepository",
    "ExportRepository",
]

###############################################################################
# Runtime
###############################################################################

def diagnostics() -> dict:
    """
    Repository package diagnostics.
    """

    return {
        "package": "repositories",
        "version": __version__,
        "repository_count": len(__all__),
        "repositories": __all__,
    }


###############################################################################


def summary() -> dict:
    """
    Repository package summary.
    """

    return {
        "name": "Sentinel AI Repository Layer",
        "version": __version__,
        "total_repositories": len(__all__),
    }


###############################################################################
# Utilities
###############################################################################

def available_repositories() -> list[str]:
    """
    Return available repositories.
    """

    return list(__all__)