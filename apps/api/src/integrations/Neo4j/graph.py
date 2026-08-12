"""
Neo4j Graph Manager
===================
"""

from __future__ import annotations

from typing import Dict, Optional


class GraphManager:

    ###########################################################################
    # Initialization
    ###########################################################################

    def __init__(self, client):

        self.client = client

    ###########################################################################
    # Graph Operations
    ###########################################################################

    def clear(self):

        return self.client.execute(
            """
            MATCH (n)
            DETACH DELETE n
            """
        )

    ###########################################################################

    def statistics(self):

        query = """
        MATCH (n)
        RETURN count(n) AS nodes
        """

        return self.client.fetch_one(query)

    ###########################################################################

    def relationships(self):

        query = """
        MATCH ()-[r]->()
        RETURN count(r) AS relationships
        """

        return self.client.fetch_one(query)

    ###########################################################################

    def shortest_path(
        self,
        source: str,
        target: str,
    ):

        query = """
        MATCH (a {address:$source}),
              (b {address:$target})
        MATCH p = shortestPath((a)-[*]-(b))
        RETURN p
        """

        return self.client.fetch_one(
            query,
            {
                "source": source,
                "target": target,
            },
        )

    ###########################################################################

    def connected_component(
        self,
        wallet: str,
    ):

        query = """
        MATCH (w {address:$wallet})-[*]-(x)
        RETURN x
        """

        return self.client.fetch_all(
            query,
            {
                "wallet": wallet,
            },
        )

    ###########################################################################

    def diagnostics(self):

        return {
            "component": "GraphManager",
        }

    ###########################################################################

    def summary(self):

        return {
            "graph": "ready",
        }


###############################################################################
# Utilities
###############################################################################


def graph_metadata():

    return {
        "database": "Neo4j",
    }