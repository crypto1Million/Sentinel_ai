"""
Helius Integration Package
==========================

Exports all Helius integration components used by Sentinel AI.
"""

###############################################################################
# Imports
###############################################################################

from .client import HeliusClient
from .rpc import HeliusRPC
from .websocket import HeliusWebSocket
from .parser import HeliusParser
from .models import (
    TransactionModel,
    WalletModel,
    TokenModel,
    AssetModel,
    InstructionModel,
    MetadataModel,
    BalanceModel,
    WebSocketEvent,
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
        "package": "integrations.helius",
        "version": __version__,
        "status": "healthy",
        "components": len(available_integrations()),
    }


def summary() -> dict:
    """
    Package summary.
    """

    return {
        "package": "integrations.helius",
        "exports": available_integrations(),
    }


###############################################################################
# Utilities
###############################################################################


def available_integrations() -> list[str]:
    """
    Returns all exported Helius integration components.
    """

    return [
        "HeliusClient",
        "HeliusRPC",
        "HeliusWebSocket",
        "HeliusParser",
        "TransactionModel",
        "WalletModel",
        "TokenModel",
        "AssetModel",
        "InstructionModel",
        "MetadataModel",
        "BalanceModel",
        "WebSocketEvent",
    ]


###############################################################################
# Public Exports
###############################################################################

__all__ = [
    "HeliusClient",
    "HeliusRPC",
    "HeliusWebSocket",
    "HeliusParser",
    "TransactionModel",
    "WalletModel",
    "TokenModel",
    "AssetModel",
    "InstructionModel",
    "MetadataModel",
    "BalanceModel",
    "WebSocketEvent",
    "available_integrations",
    "diagnostics",
    "summary",
]