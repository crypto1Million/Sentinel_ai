"""
Neo4j Graph Analytics
=====================

Advanced graph analytics for Sentinel AI.
"""

from __future__ import annotations

from typing import Any, Dict, List


###############################################################################
# GraphAnalytics
###############################################################################


class GraphAnalytics:

    ###########################################################################
    # Initialization
    ###########################################################################

    def __init__(self, client):

        self.client = client

    ###########################################################################
    # Centrality
    ###########################################################################

    def pagerank(self):

        return self.client.fetch_all(
            """
            CALL gds.pageRank.stream('walletGraph')
            YIELD nodeId, score
            RETURN gds.util.asNode(nodeId), score
            ORDER BY score DESC
            """
        )

    ###########################################################################

    def betweenness(self):

        return self.client.fetch_all(
            """
            CALL gds.betweenness.stream('walletGraph')
            """
        )

    ###########################################################################

    def closeness(self):

        return self.client.fetch_all(
            """
            CALL gds.closeness.stream('walletGraph')
            """
        )

    ###########################################################################

    def degree(self):

        return self.client.fetch_all(
            """
            CALL gds.degree.stream('walletGraph')
            """
        )

    ###########################################################################

    def eigenvector(self):

        return self.client.fetch_all(
            """
            CALL gds.eigenvector.stream('walletGraph')
            """
        )

    ###########################################################################
    # Community Detection
    ###########################################################################

    def louvain(self):

        return self.client.fetch_all(
            """
            CALL gds.louvain.stream('walletGraph')
            """
        )

    ###########################################################################

    def label_propagation(self):

        return self.client.fetch_all(
            """
            CALL gds.labelPropagation.stream('walletGraph')
            """
        )

    ###########################################################################

    def weakly_connected(self):

        return self.client.fetch_all(
            """
            CALL gds.wcc.stream('walletGraph')
            """
        )

    ###########################################################################

    def strongly_connected(self):

        return self.client.fetch_all(
            """
            CALL gds.scc.stream('walletGraph')
            """
        )

    ###########################################################################

    def community_statistics(self):

        return {
            "louvain": len(self.louvain()),
            "weak": len(self.weakly_connected()),
            "strong": len(self.strongly_connected()),
        }

    ###########################################################################
    # Path Analysis
    ###########################################################################

    def shortest_path(
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

    def all_paths(
        self,
        source: str,
        target: str,
    ):

        return self.client.fetch_all(
            """
            MATCH p=allShortestPaths(
            (:Wallet {address:$source})-[*]-(:Wallet {address:$target}))
            RETURN p
            """,
            {
                "source": source,
                "target": target,
            },
        )

    ###########################################################################

    def funding_path(
        self,
        source: str,
        target: str,
    ):

        return self.client.fetch_all(
            """
            MATCH p=
            (:Wallet {address:$source})-[:FUNDED*]->
            (:Wallet {address:$target})
            RETURN p
            """,
            {
                "source": source,
                "target": target,
            },
        )

    ###########################################################################

    def deployer_path(
        self,
        deployer: str,
    ):

        return self.client.fetch_all(
            """
            MATCH p=
            (:Deployer {wallet:$wallet})-[:DEPLOYED*]-()
            RETURN p
            """,
            {
                "wallet": deployer,
            },
        )

    ###########################################################################

    def bundle_path(
        self,
        bundle: str,
    ):

        return self.client.fetch_all(
            """
            MATCH p=
            (:Bundle {bundle_id:$bundle})-[*]-()
            RETURN p
            """,
            {
                "bundle": bundle,
            },
        )

    ###########################################################################
    # Risk Analysis
    ###########################################################################

    def rug_clusters(self):

        return self.client.fetch_all(
            """
            MATCH (w)-[:FUNDED]->(x)
            WHERE w.risk > 80
            RETURN w,x
            """
        )

    ###########################################################################

    def suspicious_wallets(self):

        return self.client.fetch_all(
            """
            MATCH (w:Wallet)
            WHERE w.score < 30
            RETURN w
            """
        )

    ###########################################################################

    def funding_cycles(self):

        return self.client.fetch_all(
            """
            MATCH p=(a)-[:FUNDED*]->(a)
            RETURN p
            """
        )

    ###########################################################################

    def circular_transfers(self):

        return self.client.fetch_all(
            """
            MATCH p=(a)-[:TRANSFERRED*]->(a)
            RETURN p
            """
        )

    ###########################################################################

    def whale_clusters(self):

        return self.client.fetch_all(
            """
            MATCH (w:Wallet)
            WHERE w.balance > 1000
            RETURN w
            """
        )

    ###########################################################################

    def smart_money_clusters(self):

        return self.client.fetch_all(
            """
            MATCH (w:Wallet)
            WHERE w.smart_money = true
            RETURN w
            """
        )

    ###########################################################################
    # Runtime
    ###########################################################################

    def diagnostics(self):

        return {
            "component": "GraphAnalytics",
        }

    ###########################################################################

    def summary(self):

        return {
            "analytics": "ready",
        }


###############################################################################
# Utilities
###############################################################################


def normalize_graph(records: List[Any]):

    return [dict(r) for r in records]


###############################################################################


def analytics_metadata():

    return {
        "engine": "Neo4j GDS",
        "algorithms": [
            "PageRank",
            "Betweenness",
            "Closeness",
            "Louvain",
            "SCC",
            "WCC",
        ],
    }