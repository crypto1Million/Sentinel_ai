"""
Mock Neo4j Integration
======================

Fake Neo4j graph database used by Sentinel AI tests.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any


class MockNeo4j:

    def __init__(self):

        self.nodes: dict[str, dict[str, Any]] = {}
        self.relationships: list[dict[str, Any]] = []

    # ------------------------------------------------------------------
    # Nodes
    # ------------------------------------------------------------------

    def create_node(
        self,
        node_id: str,
        node_type: str,
        properties: dict[str, Any] | None = None,
    ):

        node = {
            "id": node_id,
            "type": node_type,
            "properties": properties or {},
        }

        self.nodes[node_id] = node

        return node

    def get_node(
        self,
        node_id: str,
    ):

        return self.nodes.get(node_id)

    def node_exists(
        self,
        node_id: str,
    ):

        return node_id in self.nodes

    def delete_node(
        self,
        node_id: str,
    ):

        if node_id not in self.nodes:
            return False

        del self.nodes[node_id]

        self.relationships = [
            relationship
            for relationship in self.relationships
            if (
                relationship["from"] != node_id
                and relationship["to"] != node_id
            )
        ]

        return True

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------

    def create_relationship(
        self,
        source: str,
        target: str,
        relationship_type: str,
        properties: dict[str, Any] | None = None,
    ):

        relationship = {
            "from": source,
            "to": target,
            "type": relationship_type,
            "properties": properties or {},
        }

        self.relationships.append(relationship)

        return relationship

    def relationship_exists(
        self,
        source: str,
        target: str,
        relationship_type: str | None = None,
    ):

        return any(
            relationship["from"] == source
            and relationship["to"] == target
            and (
                relationship_type is None
                or relationship["type"] == relationship_type
            )
            for relationship in self.relationships
        )

    # ------------------------------------------------------------------
    # Graph Operations
    # ------------------------------------------------------------------

    def neighbors(
        self,
        node_id: str,
    ):

        result = []

        for relationship in self.relationships:

            if relationship["from"] == node_id:

                node = self.get_node(
                    relationship["to"]
                )

                if node:
                    result.append(node)

            elif relationship["to"] == node_id:

                node = self.get_node(
                    relationship["from"]
                )

                if node:
                    result.append(node)

        return result

    def shortest_path(
        self,
        source: str,
        target: str,
    ):

        if (
            source not in self.nodes
            or target not in self.nodes
        ):
            return []

        adjacency = defaultdict(list)

        for relationship in self.relationships:

            adjacency[
                relationship["from"]
            ].append(
                relationship["to"]
            )

            adjacency[
                relationship["to"]
            ].append(
                relationship["from"]
            )

        queue = [[source]]
        visited = {source}

        while queue:

            path = queue.pop(0)

            current = path[-1]

            if current == target:
                return path

            for neighbor in adjacency[current]:

                if neighbor not in visited:

                    visited.add(neighbor)

                    queue.append(
                        path + [neighbor]
                    )

        return []

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------

    def search(
        self,
        query: str,
    ):

        query = query.lower()

        results = []

        for node in self.nodes.values():

            if query in node["id"].lower():

                results.append(node)
                continue

            if query in node["type"].lower():

                results.append(node)
                continue

            if any(
                query in str(value).lower()
                for value in node["properties"].values()
            ):

                results.append(node)

        return results

    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------

    def statistics(self):

        node_types = defaultdict(int)
        relationship_types = defaultdict(int)

        for node in self.nodes.values():

            node_types[node["type"]] += 1

        for relationship in self.relationships:

            relationship_types[
                relationship["type"]
            ] += 1

        return {
            "nodes": len(self.nodes),
            "relationships": len(self.relationships),
            "node_types": dict(node_types),
            "relationship_types": dict(
                relationship_types
            ),
        }

    # ------------------------------------------------------------------
    # Runtime
    # ------------------------------------------------------------------

    def diagnostics(self):

        return {
            "connected": True,
            "nodes": len(self.nodes),
            "relationships": len(
                self.relationships
            ),
        }

    def summary(self):

        return {
            "service": "mock-neo4j",
            **self.statistics(),
        }


# ----------------------------------------------------------------------
# Factory
# ----------------------------------------------------------------------

def mock_neo4j() -> MockNeo4j:

    graph = MockNeo4j()

    graph.create_node(
        "Wallet001",
        "wallet",
        {
            "balance": 25.4,
            "score": 94,
        },
    )

    graph.create_node(
        "Wallet002",
        "wallet",
        {
            "balance": 12.7,
            "score": 72,
        },
    )

    graph.create_node(
        "TOKEN001",
        "token",
        {
            "symbol": "TMEME",
            "sentinel_score": 91,
        },
    )

    graph.create_node(
        "BUNDLE001",
        "bundle",
        {
            "percentage": 8.4,
        },
    )

    graph.create_node(
        "Deployer001",
        "deployer",
        {
            "wallet": "Wallet001",
        },
    )

    graph.create_relationship(
        "Wallet001",
        "Wallet002",
        "FUNDED",
    )

    graph.create_relationship(
        "Wallet001",
        "TOKEN001",
        "BOUGHT",
    )

    graph.create_relationship(
        "BUNDLE001",
        "TOKEN001",
        "BUNDLED",
    )

    graph.create_relationship(
        "Deployer001",
        "TOKEN001",
        "DEPLOYED",
    )

    return graph