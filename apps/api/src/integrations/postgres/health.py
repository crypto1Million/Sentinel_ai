"""
PostgreSQL Health Monitor
=========================
"""

from __future__ import annotations

import time
from sqlalchemy import text


###############################################################################
# DatabaseHealth
###############################################################################


class DatabaseHealth:

    def __init__(self, connection):

        self.connection = connection

    ###########################################################################

    def ping(self):

        start = time.perf_counter()

        with self.connection.session() as session:

            session.execute(
                text("SELECT 1")
            )

        latency = (
            time.perf_counter() - start
        ) * 1000

        return {
            "healthy": True,
            "latency_ms": round(
                latency,
                2,
            ),
        }

    ###########################################################################

    def connections(self):

        with self.connection.session() as session:

            result = session.execute(
                text(
                    """
                    SELECT count(*)
                    FROM pg_stat_activity
                    """
                )
            )

            return result.scalar()

    ###########################################################################

    def database_size(self):

        with self.connection.session() as session:

            result = session.execute(
                text(
                    """
                    SELECT pg_database_size(current_database())
                    """
                )
            )

            return result.scalar()

    ###########################################################################

    def diagnostics(self):

        return {
            "ping": self.ping(),
            "connections": self.connections(),
            "database_size": self.database_size(),
        }

    ###########################################################################

    def summary(self):

        return {
            "provider": "PostgreSQL",
            "status": "healthy",
        }


###############################################################################
# Utilities
###############################################################################


def health_metadata():

    return {
        "checks": [
            "ping",
            "connections",
            "database_size",
        ]
    }