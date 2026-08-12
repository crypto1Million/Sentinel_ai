"""
Raydium Integration Package
===========================

Exports all Raydium integration modules for Sentinel AI.
"""

###############################################################################
# Imports
###############################################################################

from .client import RaydiumClient
from .pools import PoolManager
from .swaps import SwapManager
from .liquidity import LiquidityManager
from .parser import RaydiumParser

from .models import (
    PoolModel,
    TokenModel,
    SwapModel,
    LiquidityModel,
    APRModel,
    FeeModel,
    VolumeModel,
    PositionModel,
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
        "package": "integrations.raydium",
        "version": __version__,
        "status": "healthy",
        "modules": len(available_modules()),
    }


###############################################################################


def summary() -> dict:
    """
    Package summary.
    """

    return {
        "package": "integrations.raydium",
        "exports": available_modules(),
    }


###############################################################################
# Utilities
###############################################################################


def available_modules() -> list[str]:
    """
    Returns exported modules.
    """

    return [
        "RaydiumClient",
        "PoolManager",
        "SwapManager",
        "LiquidityManager",
        "RaydiumParser",
        "PoolModel",
        "TokenModel",
        "SwapModel",
        "LiquidityModel",
        "APRModel",
        "FeeModel",
        "VolumeModel",
        "PositionModel",
    ]


###############################################################################
# Public Exports
###############################################################################

__all__ = [
    "RaydiumClient",
    "PoolManager",
    "SwapManager",
    "LiquidityManager",
    "RaydiumParser",
    "PoolModel",
    "TokenModel",
    "SwapModel",
    "LiquidityModel",
    "APRModel",
    "FeeModel",
    "VolumeModel",
    "PositionModel",
    "available_modules",
    "diagnostics",
    "summary",
]