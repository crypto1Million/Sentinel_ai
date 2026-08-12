"""
WalletDNA WebSocket Package

Real-time streaming layer for WalletDNA.

Exports all WebSocket routers so they can be
registered inside FastAPI.
"""

###############################################################################
# Wallet Stream
###############################################################################

from .wallet_stream import router as wallet_stream

###############################################################################
# Graph Stream
###############################################################################

from .graph_stream import router as graph_stream

###############################################################################
# Funding Stream
###############################################################################

from .funding_stream import router as funding_stream

###############################################################################
# Statistics Stream
###############################################################################

from .statistics_stream import router as statistics_stream

###############################################################################
# Alerts Stream
###############################################################################

from .alerts_stream import router as alerts_stream

###############################################################################
# Exports
###############################################################################

__all__ = [
    "wallet_stream",
    "graph_stream",
    "funding_stream",
    "statistics_stream",
    "alerts_stream",
]

###############################################################################
# Summary
###############################################################################

WEBSOCKET_MODULES = len(__all__)

PACKAGE_NAME = "WalletDNA WebSocket"

PACKAGE_VERSION = "1.0.0"