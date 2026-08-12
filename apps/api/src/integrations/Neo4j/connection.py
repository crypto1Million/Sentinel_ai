"""
Neo4j Connection
================
"""

from __future__ import annotations

from neo4j import GraphDatabase


###############################################################################
# Neo4jConnection
###############################################################################


class Neo4jConnection:

    ###########################################################################
    # Initialization
    ###########################################################################

    def __init__(
        self,
        uri: str,
        username: str,
        password: str,
    ):

        self.uri = uri

        self.username = username

        self.password = password

        self.driver = None

    ###########################################################################
    # Connection
    ###########################################################################

    def connect(self):

        self.driver = GraphDatabase.driver(
            self.uri,
            auth=(
                self.username,
                self.password,
            ),
        )

        self.driver.verify_connectivity()

        return self.driver

    ###########################################################################

    def disconnect(self):

        if self.driver:

            self.driver.close()

            self.driver = None

    ###########################################################################

    def session(self):

        return self.driver.session()

    ###########################################################################

    @property
    def is_connected(self):

        return self.driver is not None

    ###########################################################################

    def health(self):

        return {
            "healthy": self.is_connected,
            "uri": self.uri,
        }

    ###########################################################################

    def diagnostics(self):

        return {
            "driver": str(self.driver),
        }

    ###########################################################################

    def summary(self):

        return {
            "database": "Neo4j",
            "connected": self.is_connected,
        }


###############################################################################
# Utilities
###############################################################################


def connection_url(
    host: str,
    port: int,
):

    return f"bolt://{host}:{port}"