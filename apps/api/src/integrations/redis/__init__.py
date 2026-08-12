"""
Redis Integration
=================

Exports Redis integration modules for Sentinel AI.
"""

###############################################################################
# Imports
###############################################################################

from .client import RedisClient
from .cache import CacheManager
from .pubsub import PubSubManager
from .streams import StreamManager
from .locks import LockManager
from .parser import RedisParser

from .models import (
    CacheEntryModel,
    PubSubMessageModel,
    StreamMessageModel,
    LockModel,
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
    Integration diagnostics.
    """

    return {
        "integration": "Redis",
        "version": __version__,
        "status": "healthy",
        "modules": len(available_integrations()),
    }


###############################################################################


def summary() -> dict:
    """
    Integration summary.
    """

    return {
        "integration": "Redis",
        "exports": available_integrations(),
    }


###############################################################################
# Utilities
###############################################################################


def available_integrations() -> list[str]:
    """
    Exported Redis components.
    """

    return [
        "RedisClient",
        "CacheManager",
        "PubSubManager",
        "StreamManager",
        "LockManager",
        "RedisParser",
        "CacheEntryModel",
        "PubSubMessageModel",
        "StreamMessageModel",
        "LockModel",
    ]


###############################################################################
# Public Exports
###############################################################################

__all__ = [
    "RedisClient",
    "CacheManager",
    "PubSubManager",
    "StreamManager",
    "LockManager",
    "RedisParser",
    "CacheEntryModel",
    "PubSubMessageModel",
    "StreamMessageModel",
    "LockModel",
    "available_integrations",
    "diagnostics",
    "summary",
]