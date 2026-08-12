"""
PostgreSQL Integration
======================

Exports PostgreSQL integration layer for Sentinel AI.
"""

###############################################################################
# Imports
###############################################################################

from .client import PostgreSQLClient
from .connection import PostgreSQLConnection

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
    PostgreSQL integration diagnostics.
    """

    return {
        "integration": "PostgreSQL",
        "version": __version__,
        "status": "healthy",
        "modules": len(available_integrations()),
    }


###############################################################################


def summary() -> dict:
    """
    PostgreSQL integration summary.
    """

    return {
        "integration": "PostgreSQL",
        "exports": available_integrations(),
    }


###############################################################################
# Utilities
###############################################################################


def available_integrations() -> list[str]:
    """
    Exported PostgreSQL components.
    """

    return [
        "PostgreSQLClient",
        "PostgreSQLConnection",
    ]


###############################################################################
# Public Exports
###############################################################################

__all__ = [
    "PostgreSQLClient",
    "PostgreSQLConnection",
    "available_integrations",
    "diagnostics",
    "summary",
]