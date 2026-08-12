"""
redis_workers package
=====================

Exports all Redis worker implementations used by Sentinel AI.
"""

###############################################################################
# Imports
###############################################################################

from .wallet_worker import WalletWorker
from .funding_worker import FundingWorker
from .bundle_worker import BundleWorker
from .statistics_worker import StatisticsWorker
from .runtime_worker import RuntimeWorker

###############################################################################
# Version
###############################################################################

__version__ = "1.0.0"
__author__ = "Sentinel AI"

###############################################################################
# Runtime
###############################################################################


def diagnostics() -> dict:
    """
    Package diagnostics.
    """

    return {
        "package": "redis_workers",
        "version": __version__,
        "workers": len(available_workers()),
        "status": "healthy",
    }


def summary() -> dict:
    """
    Package summary.
    """

    return {
        "package": "redis_workers",
        "available_workers": available_workers(),
    }


###############################################################################
# Utilities
###############################################################################


def available_workers() -> list[str]:
    """
    List all available worker classes.
    """

    return [
        "WalletWorker",
        "FundingWorker",
        "BundleWorker",
        "StatisticsWorker",
        "RuntimeWorker",
    ]


###############################################################################
# Public Exports
###############################################################################

__all__ = [
    "WalletWorker",
    "FundingWorker",
    "BundleWorker",
    "StatisticsWorker",
    "RuntimeWorker",
    "available_workers",
    "diagnostics",
    "summary",
]