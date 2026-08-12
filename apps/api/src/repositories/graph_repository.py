###############################################################################
# Imports
###############################################################################

from __future__ import annotations

from .neo4j_repository import Neo4jRepository

###############################################################################
# GraphRepository
###############################################################################


class GraphRepository(Neo4jRepository):
    """
    Graph Repository.
    """

    ###########################################################################
    # Initialization
    ###########################################################################

    def __init__(self, driver):

        super().__init__(driver)

    ###########################################################################
    # CRUD
    ###########################################################################

    def get_graph(
        self,
        graph_id: str,
    ):

        return self.find_node(
            graph_id,
        )

    ###########################################################################

    def create_graph(
        self,
        node: dict,
    ):

        return self.create_node(
            node,
        )

    ###########################################################################

    def update_graph(
        self,
        graph_id: str,
        values: dict,
    ):

        return self.update_node(
            graph_id,
            values,
        )

    ###########################################################################

    def delete_graph(
        self,
        graph_id: str,
    ):

        return self.delete_node(
            graph_id,
        )

    ###########################################################################

    def graph_exists(
        self,
        graph_id: str,
    ):

        return self.find_node(
            graph_id,
        ) is not None

    ###########################################################################
    # Nodes
    ###########################################################################

    def graph_nodes(
        self,
        graph_id: str,
    ):

        return self.execute(
            """
            MATCH (n {graph_id:$graph_id})
            RETURN n
            """,
            {
                "graph_id": graph_id,
            },
        )

    ###########################################################################

    def graph_edges(
        self,
        graph_id: str,
    ):

        return self.execute(
            """
            MATCH ()-[r {graph_id:$graph_id}]-()
            RETURN r
            """,
            {
                "graph_id": graph_id,
            },
        )

    ###########################################################################

    def graph_neighbors(
        self,
        node_id: str,
    ):

        return self.neighbors(
            node_id,
        )

    ###########################################################################

    def shortest_path(
        self,
        start: str,
        end: str,
    ):

        return super().shortest_path(
            start,
            end,
        )

    ###########################################################################

    def connected_components(self):

        return super().connected_components()

    ###########################################################################

    def subgraph(
        self,
        node_id: str,
        depth: int = 2,
    ):

        return super().subgraph(
            node_id,
            depth,
        )

    ###########################################################################
    # Analytics
    ###########################################################################

    def graph_statistics(self):

        return self.execute(
            """
            MATCH (n)
            OPTIONAL MATCH ()-[r]->()
            RETURN count(DISTINCT n) AS nodes,
                   count(DISTINCT r) AS edges
            """
        )

    ###########################################################################

    def wallet_graph(
        self,
        wallet: str,
    ):

        return self.execute(
            """
            MATCH (w:Wallet {address:$wallet})-[r*1..3]-(n)
            RETURN w,r,n
            """,
            {
                "wallet": wallet,
            },
        )

    ###########################################################################

    def token_graph(
        self,
        mint: str,
    ):

        return self.execute(
            """
            MATCH (t:Token {mint:$mint})-[r*1..3]-(n)
            RETURN t,r,n
            """,
            {
                "mint": mint,
            },
        )

    ###########################################################################

    def deployer_graph(
        self,
        deployer: str,
    ):

        return self.execute(
            """
            MATCH (d:Deployer {address:$deployer})-[r*1..3]-(n)
            RETURN d,r,n
            """,
            {
                "deployer": deployer,
            },
        )

    ###########################################################################

    def funding_graph(
        self,
        wallet: str,
    ):

        return self.execute(
            """
            MATCH (w:Wallet {address:$wallet})-[r:FUNDED*1..5]-(n)
            RETURN w,r,n
            """,
            {
                "wallet": wallet,
            },
        )

    ###########################################################################

    def cluster_graph(
        self,
        cluster_id: str,
    ):

        return self.execute(
            """
            MATCH (c:Cluster {id:$cluster})
            MATCH (c)-[r]-(n)
            RETURN c,r,n
            """,
            {
                "cluster": cluster_id,
            },
        )

    ###########################################################################

    def graph_score(
        self,
        graph_id: str,
    ):

        return {
            "graph": graph_id,
            "score": 0,
        }

    ###########################################################################
    # Search
    ###########################################################################

    def search_graph(
        self,
        query: str,
    ):

        return self.execute(
            """
            MATCH (n)
            WHERE toString(n) CONTAINS $query
            RETURN n
            LIMIT 100
            """,
            {
                "query": query,
            },
        )

    ###########################################################################

    def compare_graphs(
        self,
        graph_a: str,
        graph_b: str,
    ):

        return {
            "graph_a": graph_a,
            "graph_b": graph_b,
        }

    ###########################################################################
    # Export
    ###########################################################################

    def export_graph(
        self,
        graph_id: str,
    ):

        return {
            "nodes": self.graph_nodes(graph_id),
            "edges": self.graph_edges(graph_id),
        }

    ###########################################################################

    def export_graph_json(
        self,
        graph_id: str,
    ):

        return self.export_graph(
            graph_id,
        )

    ###########################################################################
    # Health
    ###########################################################################

    def health(self):

        return super().health()

    ###########################################################################

    def diagnostics(self):

        return {
            "repository": "GraphRepository",
            "healthy": self.health(),
        }


###############################################################################
# Runtime
###############################################################################


def summary():

    return {
        "repository": "GraphRepository",
    }


###############################################################################
# Utilities
###############################################################################


def normalize_graph(
    graph_id: str,
):

    return graph_id.strip()


###############################################################################


def build_graph(
    nodes,
    edges,
):

    return {
        "nodes": nodes,
        "edges": edges,
    }


###############################################################################


def cache_graph(
    graph_id: str,
):

    return f"graph:{graph_id}"


###############################################################################


def graph_metadata(
    graph_id: str,
):

    return {
        "graph": graph_id,
    }