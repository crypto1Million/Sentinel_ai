"""
Neo4j High-Level Queries
========================
"""

from __future__ import annotations

from typing import Dict, List, Optional


###############################################################################
# GraphQueries
###############################################################################


class GraphQueries:

    ###########################################################################
    # Initialization
    ###########################################################################

    def __init__(self, client):

        self.client = client

    ###########################################################################
    # Wallet Queries
    ###########################################################################

    def wallet(
        self,
        address: str,
    ):

        query = """
        MATCH (w:Wallet {address:$address})
        RETURN w
        """

        return self.client.fetch_one(
            query,
            {"address": address},
        )

    ###########################################################################

    def wallet_graph(
        self,
        address: str,
    ):

        query = """
        MATCH p=(w:Wallet {address:$address})-[*1..5]-(x)
        RETURN p
        """

        return self.client.fetch_all(
            query,
            {"address": address},
        )

    ###########################################################################

    def wallet_funding(
        self,
        address: str,
    ):

        query = """
        MATCH (w:Wallet {address:$address})<-[r:FUNDED]-(x)
        RETURN x,r
        """

        return self.client.fetch_all(
            query,
            {"address": address},
        )

    ###########################################################################

    def wallet_clusters(
        self,
        address: str,
    ):

        query = """
        MATCH (w:Wallet {address:$address})-[*]-(x)
        RETURN DISTINCT x
        """

        return self.client.fetch_all(
            query,
            {"address": address},
        )

    ###########################################################################

    def wallet_score(
        self,
        address: str,
    ):

        query = """
        MATCH (w:Wallet {address:$address})
        RETURN w.score
        """

        return self.client.fetch_one(
            query,
            {"address": address},
        )

    ###########################################################################

    def wallet_statistics(
        self,
        address: str,
    ):

        query = """
        MATCH (w:Wallet {address:$address})--()
        RETURN count(*) AS connections
        """

        return self.client.fetch_one(
            query,
            {"address": address},
        )

    ###########################################################################
    # Token Queries
    ###########################################################################

    def token(
        self,
        mint: str,
    ):

        query = """
        MATCH (t:Token {mint:$mint})
        RETURN t
        """

        return self.client.fetch_one(
            query,
            {"mint": mint},
        )

    ###########################################################################

    def token_graph(
        self,
        mint: str,
    ):

        query = """
        MATCH p=(t:Token {mint:$mint})-[*1..5]-(x)
        RETURN p
        """

        return self.client.fetch_all(
            query,
            {"mint": mint},
        )

    ###########################################################################

    def token_holders(
        self,
        mint: str,
    ):

        query = """
        MATCH (w:Wallet)-[:OWNS]->(t:Token {mint:$mint})
        RETURN w
        """

        return self.client.fetch_all(
            query,
            {"mint": mint},
        )

    ###########################################################################

    def token_bundles(
        self,
        mint: str,
    ):

        query = """
        MATCH (t:Token {mint:$mint})<-[:CONTAINS]-(b:Bundle)
        RETURN b
        """

        return self.client.fetch_all(
            query,
            {"mint": mint},
        )

    ###########################################################################

    def token_deployer(
        self,
        mint: str,
    ):

        query = """
        MATCH (d:Deployer)-[:DEPLOYED]->(t:Token {mint:$mint})
        RETURN d
        """

        return self.client.fetch_one(
            query,
            {"mint": mint},
        )

    ###########################################################################

    def token_score(
        self,
        mint: str,
    ):

        query = """
        MATCH (t:Token {mint:$mint})
        RETURN t.score
        """

        return self.client.fetch_one(
            query,
            {"mint": mint},
        )

    ###########################################################################

    def token_statistics(
        self,
        mint: str,
    ):

        query = """
        MATCH (w)-[:OWNS]->(t:Token {mint:$mint})
        RETURN count(w) AS holders
        """

        return self.client.fetch_one(
            query,
            {"mint": mint},
        )

    ###########################################################################
    # Bundle Queries
    ###########################################################################

    def bundle(
        self,
        bundle_id: str,
    ):

        return self.client.fetch_one(
            """
            MATCH (b:Bundle {bundle_id:$bundle})
            RETURN b
            """,
            {"bundle": bundle_id},
        )

    ###########################################################################

    def bundle_graph(
        self,
        bundle_id: str,
    ):

        return self.client.fetch_all(
            """
            MATCH p=(b:Bundle {bundle_id:$bundle})-[*]-(x)
            RETURN p
            """,
            {"bundle": bundle_id},
        )

    ###########################################################################

    def bundle_wallets(
        self,
        bundle_id: str,
    ):

        return self.client.fetch_all(
            """
            MATCH (w)-[:BUNDLED]->(b:Bundle {bundle_id:$bundle})
            RETURN w
            """,
            {"bundle": bundle_id},
        )

    ###########################################################################

    def bundle_score(
        self,
        bundle_id: str,
    ):

        return self.client.fetch_one(
            """
            MATCH (b:Bundle {bundle_id:$bundle})
            RETURN b.score
            """,
            {"bundle": bundle_id},
        )

    ###########################################################################

    def bundle_statistics(
        self,
        bundle_id: str,
    ):

        return self.client.fetch_one(
            """
            MATCH (w)-[:BUNDLED]->(b:Bundle {bundle_id:$bundle})
            RETURN count(w)
            """,
            {"bundle": bundle_id},
        )

    ###########################################################################
    # Graph Queries
    ###########################################################################

    def graph(self):

        return self.client.fetch_all(
            """
            MATCH p=()-[*]->()
            RETURN p
            LIMIT 100
            """
        )

    ###########################################################################

    def graph_overview(self):

        return self.client.fetch_one(
            """
            MATCH (n)
            OPTIONAL MATCH ()-[r]->()
            RETURN count(distinct n) AS nodes,
                   count(r) AS relationships
            """
        )

    ###########################################################################

    def graph_search(
        self,
        query_string: str,
    ):

        return self.client.fetch_all(
            """
            MATCH (n)
            WHERE ANY(
                k IN keys(n)
                WHERE toString(n[k]) CONTAINS $query
            )
            RETURN n
            """,
            {"query": query_string},
        )

    ###########################################################################

    def graph_paths(
        self,
        source: str,
        target: str,
    ):

        return self.client.fetch_one(
            """
            MATCH p=shortestPath(
            (:Wallet {address:$source})-[*]-(:Wallet {address:$target}))
            RETURN p
            """,
            {
                "source": source,
                "target": target,
            },
        )

    ###########################################################################

    def graph_clusters(self):

        return self.client.fetch_all(
            """
            MATCH (n)-[*]-(m)
            RETURN n,m
            LIMIT 100
            """
        )

    ###########################################################################

    def graph_statistics(self):

        return self.graph_overview()

    ###########################################################################
    # Runtime
    ###########################################################################

    def diagnostics(self):

        return {
            "component": "GraphQueries",
        }

    ###########################################################################

    def summary(self):

        return {
            "queries": "ready",
        }


###############################################################################
# Utilities
###############################################################################


def normalize_result(record):

    if record is None:

        return None

    return dict(record)


###############################################################################


def query_metadata():

    return {
        "database": "Neo4j",
        "language": "Cypher",
    }