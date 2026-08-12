"""
Neo4j Integration
=================

Exports Neo4j integration modules for Sentinel AI.
"""

###############################################################################
# Imports
###############################################################################

from .client import Neo4jClient
from .connection import Neo4jConnection

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
    Neo4j integration diagnostics.
    """

    return {
        "integration": "Neo4j",
        "version": __version__,
        "status": "healthy",
        "modules": len(available_integrations()),
    }


###############################################################################


def summary() -> dict:
    """
    Neo4j integration summary.
    """

    return {
        "integration": "Neo4j",
        "exports": available_integrations(),
    }


###############################################################################
# Utilities
###############################################################################


def available_integrations() -> list[str]:

    return [
        "Neo4jClient",
        "Neo4jConnection",
    ]


###############################################################################
# Public Exports
###############################################################################

__all__ = [
    "Neo4jClient",
    "Neo4jConnection",
    "available_integrations",
    "diagnostics",
    "summary",
]