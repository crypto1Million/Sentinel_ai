"""
DexScreener Integration Package
===============================

Exports all DexScreener integration modules for Sentinel AI.
"""

###############################################################################
# Imports
###############################################################################

from .client import DexScreenerClient
from .pairs import PairManager
from .search import SearchManager
from .parser import DexParser

from .models import (
    PairModel,
    TokenModel,
    PriceModel,
    LiquidityModel,
    VolumeModel,
    HolderModel,
    TransactionModel,
    SearchModel,
)

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
        "package": "integrations.dexscreener",
        "version": __version__,
        "status": "healthy",
        "modules": len(available_modules()),
    }


def summary() -> dict:
    """
    Package summary.
    """

    return {
        "package": "integrations.dexscreener",
        "exports": available_modules(),
    }


###############################################################################
# Utilities
###############################################################################


def available_modules() -> list[str]:
    """
    Returns all exported modules.
    """

    return [
        "DexScreenerClient",
        "PairManager",
        "SearchManager",
        "DexParser",
        "PairModel",
        "TokenModel",
        "PriceModel",
        "LiquidityModel",
        "VolumeModel",
        "HolderModel",
        "TransactionModel",
        "SearchModel",
    ]


###############################################################################
# Public Exports
###############################################################################

__all__ = [
    "DexScreenerClient",
    "PairManager",
    "SearchManager",
    "DexParser",
    "PairModel",
    "TokenModel",
    "PriceModel",
    "LiquidityModel",
    "VolumeModel",
    "HolderModel",
    "TransactionModel",
    "SearchModel",
    "available_modules",
    "diagnostics",
    "summary",
]