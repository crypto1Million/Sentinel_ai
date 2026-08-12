"""
Cypher Query Builder
====================

Reusable Cypher query generator for Sentinel AI.
"""

from __future__ import annotations

from typing import Dict, List, Optional


###############################################################################
# CypherBuilder
###############################################################################


class CypherBuilder:

    ###########################################################################
    # Node Queries
    ###########################################################################

    def create_node(
        self,
        label: str,
    ):

        return f"""
        CREATE (n:{label})
        SET n += $properties
        RETURN n
        """

    ###########################################################################

    def merge_node(
        self,
        label: str,
        key: str,
    ):

        return f"""
        MERGE (n:{label} {{{key}:$value}})
        SET n += $properties
        RETURN n
        """

    ###########################################################################

    def update_node(
        self,
        label: str,
        key: str,
    ):

        return f"""
        MATCH (n:{label} {{{key}:$value}})
        SET n += $properties
        RETURN n
        """

    ###########################################################################

    def delete_node(
        self,
        label: str,
        key: str,
    ):

        return f"""
        MATCH (n:{label} {{{key}:$value}})
        DETACH DELETE n
        """

    ###########################################################################

    def find_node(
        self,
        label: str,
        key: str,
    ):

        return f"""
        MATCH (n:{label} {{{key}:$value}})
        RETURN n
        """

    ###########################################################################

    def node_exists(
        self,
        label: str,
        key: str,
    ):

        return f"""
        MATCH (n:{label} {{{key}:$value}})
        RETURN COUNT(n)>0 AS exists
        """

    ###########################################################################
    # Relationship Queries
    ###########################################################################

    def create_relationship(
        self,
        source_label: str,
        relationship: str,
        target_label: str,
    ):

        return f"""
        MATCH (a:{source_label} {{address:$source}})
        MATCH (b:{target_label} {{address:$target}})
        CREATE (a)-[r:{relationship}]->(b)
        SET r += $properties
        RETURN r
        """

    ###########################################################################

    def merge_relationship(
        self,
        source_label: str,
        relationship: str,
        target_label: str,
    ):

        return f"""
        MATCH (a:{source_label} {{address:$source}})
        MATCH (b:{target_label} {{address:$target}})
        MERGE (a)-[r:{relationship}]->(b)
        SET r += $properties
        RETURN r
        """

    ###########################################################################

    def update_relationship(
        self,
        relationship: str,
    ):

        return f"""
        MATCH ()-[r:{relationship}]->()
        WHERE id(r)=$id
        SET r += $properties
        RETURN r
        """

    ###########################################################################

    def delete_relationship(
        self,
        relationship: str,
    ):

        return f"""
        MATCH ()-[r:{relationship}]->()
        WHERE id(r)=$id
        DELETE r
        """

    ###########################################################################

    def relationship_exists(
        self,
        relationship: str,
    ):

        return f"""
        MATCH ()-[r:{relationship}]->()
        WHERE id(r)=$id
        RETURN COUNT(r)>0 AS exists
        """

    ###########################################################################

    def relationship_properties(
        self,
        relationship: str,
    ):

        return f"""
        MATCH ()-[r:{relationship}]->()
        WHERE id(r)=$id
        RETURN properties(r)
        """

    ###########################################################################
    # Graph Queries
    ###########################################################################

    def shortest_path(self):

        return """
        MATCH (a {address:$source}),
              (b {address:$target})
        MATCH p=shortestPath((a)-[*]-(b))
        RETURN p
        """

    ###########################################################################

    def neighbors(self):

        return """
        MATCH (n {address:$address})--(x)
        RETURN x
        """

    ###########################################################################

    def subgraph(self):

        return """
        MATCH p=(n {address:$address})-[*1..3]-(m)
        RETURN p
        """

    ###########################################################################

    def connected_component(self):

        return """
        MATCH (n {address:$address})-[*]-(m)
        RETURN m
        """

    ###########################################################################

    def graph_statistics(self):

        return """
        MATCH (n)
        OPTIONAL MATCH ()-[r]->()
        RETURN COUNT(DISTINCT n) AS nodes,
               COUNT(r) AS relationships
        """

    ###########################################################################

    def graph_cleanup(self):

        return """
        MATCH (n)
        WHERE size(labels(n))=0
        DETACH DELETE n
        """

    ###########################################################################
    # Search Queries
    ###########################################################################

    def search_wallet(self):

        return """
        MATCH (w:Wallet)
        WHERE w.address CONTAINS $query
        RETURN w
        """

    ###########################################################################

    def search_token(self):

        return """
        MATCH (t:Token)
        WHERE t.symbol CONTAINS $query
           OR t.name CONTAINS $query
        RETURN t
        """

    ###########################################################################

    def search_bundle(self):

        return """
        MATCH (b:Bundle)
        WHERE b.bundle_id CONTAINS $query
        RETURN b
        """

    ###########################################################################

    def search_deployer(self):

        return """
        MATCH (d:Deployer)
        WHERE d.wallet CONTAINS $query
        RETURN d
        """

    ###########################################################################

    def global_search(self):

        return """
        MATCH (n)
        WHERE ANY(
            k IN keys(n)
            WHERE toString(n[k]) CONTAINS $query
        )
        RETURN n
        LIMIT 100
        """

    ###########################################################################
    # Runtime
    ###########################################################################

    def diagnostics(self):

        return {
            "builder": "CypherBuilder",
        }

    ###########################################################################

    def summary(self):

        return {
            "queries": "ready",
        }


###############################################################################
# Utilities
###############################################################################


def parameterize(
    query: str,
    parameters: Dict,
):

    return {
        "query": query,
        "parameters": parameters,
    }


###############################################################################


def normalize_query(
    query: str,
):

    return " ".join(
        query.split()
    )


###############################################################################


def query_metadata():

    return {
        "language": "Cypher",
        "database": "Neo4j",
    }