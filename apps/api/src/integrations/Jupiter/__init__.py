"""
Jupiter Integration
===================

Exports all Jupiter integration modules for Sentinel AI.
"""

###############################################################################
# Imports
###############################################################################

from .client import JupiterClient
from .quotes import QuoteManager
from .swaps import SwapManager
from .routes import RouteManager
from .parser import JupiterParser

from .models import (
    QuoteModel,
    RouteModel,
    SwapModel,
    TokenModel,
    PlatformFeeModel,
    SlippageModel,
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
        "package": "integrations.jupiter",
        "version": __version__,
        "status": "healthy",
        "modules": len(available_integrations()),
    }


###############################################################################


def summary() -> dict:
    """
    Package summary.
    """

    return {
        "package": "integrations.jupiter",
        "exports": available_integrations(),
    }


###############################################################################
# Utilities
###############################################################################


def available_integrations() -> list[str]:
    """
    Available Jupiter modules.
    """

    return [
        "JupiterClient",
        "QuoteManager",
        "SwapManager",
        "RouteManager",
        "JupiterParser",
        "QuoteModel",
        "RouteModel",
        "SwapModel",
        "TokenModel",
        "PlatformFeeModel",
        "SlippageModel",
    ]


###############################################################################
# Public Exports
###############################################################################

__all__ = [
    "JupiterClient",
    "QuoteManager",
    "SwapManager",
    "RouteManager",
    "JupiterParser",
    "QuoteModel",
    "RouteModel",
    "SwapModel",
    "TokenModel",
    "PlatformFeeModel",
    "SlippageModel",
    "available_integrations",
    "diagnostics",
    "summary",
]