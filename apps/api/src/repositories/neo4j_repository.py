###############################################################################
# Imports
###############################################################################

from __future__ import annotations

from typing import Any

from neo4j import GraphDatabase
from neo4j import Driver

from .base_repository import BaseRepository

###############################################################################
# Neo4jRepository
###############################################################################


class Neo4jRepository(BaseRepository):
    """
    Neo4j Graph Repository.
    """

    ###########################################################################
    # Initialization
    ###########################################################################

    def __init__(
        self,
        uri: str,
        username: str,
        password: str,
    ) -> None:

        super().__init__(None)

        self.uri = uri
        self.username = username
        self.password = password

        self.driver: Driver | None = None

    ###########################################################################
    # Connection
    ###########################################################################

    def connect(
        self,
    ) -> None:

        self.driver = GraphDatabase.driver(
            self.uri,
            auth=(
                self.username,
                self.password,
            ),
        )

    ###########################################################################

    def disconnect(
        self,
    ) -> None:

        if self.driver:
            self.driver.close()

        self.driver = None

    ###########################################################################
    # Execution
    ###########################################################################

    def execute(
        self,
        query: str,
        parameters: dict | None = None,
    ) -> list[dict]:

        with self.driver.session() as session:

            result = session.run(
                query,
                parameters or {},
            )

            return [
                record.data()
                for record in result
            ]

    ###########################################################################
    # Nodes
    ###########################################################################

    def create_node(
        self,
        label: str,
        properties: dict,
    ):

        query = (
            f"CREATE (n:{label} $props)"
        )

        return self.execute(
            query,
            {
                "props": properties,
            },
        )

    ###########################################################################

    def create_edge(
        self,
        source: str,
        target: str,
        relationship: str,
    ):

        query = f"""
        MATCH (a {{id:$source}})
        MATCH (b {{id:$target}})
        CREATE (a)-[:{relationship}]->(b)
        """

        return self.execute(
            query,
            {
                "source": source,
                "target": target,
            },
        )

    ###########################################################################

    def update_node(
        self,
        node_id: str,
        properties: dict,
    ):

        query = """
        MATCH (n {id:$id})
        SET n += $props
        RETURN n
        """

        return self.execute(
            query,
            {
                "id": node_id,
                "props": properties,
            },
        )

    ###########################################################################

    def delete_node(
        self,
        node_id: str,
    ):

        query = """
        MATCH (n {id:$id})
        DETACH DELETE n
        """

        return self.execute(
            query,
            {
                "id": node_id,
            },
        )

    ###########################################################################

    def delete_edge(
        self,
        source: str,
        target: str,
        relationship: str,
    ):

        query = f"""
        MATCH (a {{id:$source}})
        -[r:{relationship}]->
        (b {{id:$target}})
        DELETE r
        """

        return self.execute(
            query,
            {
                "source": source,
                "target": target,
            },
        )

    ###########################################################################

    def find_node(
        self,
        node_id: str,
    ):

        query = """
        MATCH (n {id:$id})
        RETURN n
        """

        return self.execute(
            query,
            {
                "id": node_id,
            },
        )

    ###########################################################################

    def find_relationship(
        self,
        source: str,
        target: str,
    ):

        query = """
        MATCH (a {id:$source})-[r]->(b {id:$target})
        RETURN r
        """

        return self.execute(
            query,
            {
                "source": source,
                "target": target,
            },
        )

    ###########################################################################

    def shortest_path(
        self,
        source: str,
        target: str,
    ):

        query = """
        MATCH p=shortestPath(
        (a {id:$source})-[*]-(b {id:$target})
        )
        RETURN p
        """

        return self.execute(
            query,
            {
                "source": source,
                "target": target,
            },
        )

    ###########################################################################

    def connected_components(
        self,
    ):

        query = """
        CALL gds.wcc.stream('walletGraph')
        YIELD nodeId, componentId
        RETURN nodeId, componentId
        """

        return self.execute(query)

    ###########################################################################

    def neighbors(
        self,
        node_id: str,
    ):

        query = """
        MATCH (n {id:$id})--(m)
        RETURN m
        """

        return self.execute(
            query,
            {
                "id": node_id,
            },
        )

    ###########################################################################

    def subgraph(
        self,
        node_id: str,
        depth: int = 2,
    ):

        query = f"""
        MATCH p=(n {{id:$id}})-[*1..{depth}]-(m)
        RETURN p
        """

        return self.execute(
            query,
            {
                "id": node_id,
            },
        )

    ###########################################################################

    def raw_query(
        self,
        query: str,
        parameters: dict | None = None,
    ):

        return self.execute(
            query,
            parameters,
        )

    ###########################################################################
    # Health
    ###########################################################################

    def health(
        self,
    ) -> bool:

        try:

            self.execute("RETURN 1")

            return True

        except Exception:

            return False

    ###########################################################################

    def diagnostics(
        self,
    ):

        return {
            "repository": "Neo4j",
            "connected": self.driver is not None,
            "healthy": self.health(),
        }


###############################################################################
# Graph Operations
###############################################################################


def merge_wallet(
    repository: Neo4jRepository,
    wallet: dict,
):

    query = """
    MERGE (w:Wallet {id:$id})
    SET w += $props
    """

    return repository.execute(
        query,
        {
            "id": wallet["id"],
            "props": wallet,
        },
    )


###############################################################################


def merge_token(
    repository: Neo4jRepository,
    token: dict,
):

    query = """
    MERGE (t:Token {id:$id})
    SET t += $props
    """

    return repository.execute(
        query,
        {
            "id": token["id"],
            "props": token,
        },
    )


###############################################################################


def merge_cluster(
    repository: Neo4jRepository,
    cluster: dict,
):

    query = """
    MERGE (c:Cluster {id:$id})
    SET c += $props
    """

    return repository.execute(
        query,
        {
            "id": cluster["id"],
            "props": cluster,
        },
    )


###############################################################################


def merge_funding(
    repository: Neo4jRepository,
    funding: dict,
):

    query = """
    MERGE (f:Funding {id:$id})
    SET f += $props
    """

    return repository.execute(
        query,
        {
            "id": funding["id"],
            "props": funding,
        },
    )


###############################################################################


def merge_bundle(
    repository: Neo4jRepository,
    bundle: dict,
):

    query = """
    MERGE (b:Bundle {id:$id})
    SET b += $props
    """

    return repository.execute(
        query,
        {
            "id": bundle["id"],
            "props": bundle,
        },
    )


###############################################################################
# Runtime
###############################################################################


def summary():

    return {
        "repository": "Neo4j",
        "graph_database": True,
    }


###############################################################################
# Utilities
###############################################################################


def build_cypher(
    query: str,
):

    return query.strip()


###############################################################################


def sanitize_parameters(
    parameters: dict | None,
):

    return parameters or {}


###############################################################################


def explain_query(
    repository: Neo4jRepository,
    query: str,
):

    return repository.execute(
        f"EXPLAIN {query}",
    )


###############################################################################


def normalize_graph(
    graph: list[dict],
):

    return graph