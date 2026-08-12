"""
Neo4j Client
============

High-level Neo4j Client for Sentinel AI.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from neo4j import Result

from .connection import Neo4jConnection


###############################################################################
# Neo4jClient
###############################################################################


class Neo4jClient:

    ###########################################################################
    # Initialization
    ###########################################################################

    def __init__(
        self,
        connection: Neo4jConnection,
    ):

        self.connection = connection

    ###########################################################################
    # Connection
    ###########################################################################

    def connect(self):

        return self.connection.connect()

    ###########################################################################

    def disconnect(self):

        self.connection.disconnect()

    ###########################################################################

    def health(self):

        return self.connection.health()

    ###########################################################################
    # Cypher
    ###########################################################################

    def execute(
        self,
        query: str,
        parameters: Optional[Dict] = None,
    ) -> Result:

        with self.connection.session() as session:

            return session.run(
                query,
                parameters or {},
            )

    ###########################################################################

    def fetch_one(
        self,
        query: str,
        parameters: Optional[Dict] = None,
    ):

        return self.execute(
            query,
            parameters,
        ).single()

    ###########################################################################

    def fetch_all(
        self,
        query: str,
        parameters: Optional[Dict] = None,
    ):

        return list(
            self.execute(
                query,
                parameters,
            )
        )

    ###########################################################################

    def write(
        self,
        query: str,
        parameters: Optional[Dict] = None,
    ):

        return self.execute(
            query,
            parameters,
        )

    ###########################################################################
    # Runtime
    ###########################################################################

    def diagnostics(self):

        return {
            "client": "Neo4jClient",
            "connected": self.connection.is_connected,
        }

    ###########################################################################

    def summary(self):

        return {
            "provider": "Neo4j",
            "status": (
                "connected"
                if self.connection.is_connected
                else "disconnected"
            ),
        }


###############################################################################
# Utilities
###############################################################################


def normalize_records(
    records: List[Any],
):

    return [
        dict(record)
        for record in records
    ]