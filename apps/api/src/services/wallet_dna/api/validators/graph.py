###############################################################################
# Imports
###############################################################################

from __future__ import annotations

from typing import Any

###############################################################################
# Graph Validation
###############################################################################


def validate_node(
    node: dict[str, Any],
) -> bool:
    """
    Validate graph node.
    """

    required = {
        "id",
        "label",
        "type",
    }

    return required.issubset(node.keys())


###############################################################################


def validate_edge(
    edge: dict[str, Any],
) -> bool:
    """
    Validate graph edge.
    """

    required = {
        "source",
        "target",
        "relationship",
    }

    return required.issubset(edge.keys())


###############################################################################


def validate_graph(
    graph: dict[str, Any],
) -> bool:
    """
    Validate complete graph.
    """

    if "nodes" not in graph or "edges" not in graph:
        return False

    return (
        all(validate_node(node) for node in graph["nodes"])
        and all(validate_edge(edge) for edge in graph["edges"])
    )


###############################################################################


def validate_cluster(
    cluster: dict[str, Any],
) -> bool:
    """
    Validate cluster payload.
    """

    required = {
        "cluster_id",
        "wallets",
    }

    return required.issubset(cluster.keys())


###############################################################################


def validate_graph_request(
    request: dict[str, Any],
) -> bool:
    """
    Validate graph API request.
    """

    return "graph_id" in request or "wallet" in request or "token" in request


###############################################################################
# Runtime
###############################################################################


def diagnostics() -> dict[str, Any]:
    """
    Validator diagnostics.
    """

    return {
        "validator": "graph",
        "status": "healthy",
    }


###############################################################################


def summary() -> dict[str, Any]:
    """
    Validator summary.
    """

    return {
        "node_validation": True,
        "edge_validation": True,
        "cluster_validation": True,
    }


###############################################################################
# Utilities
###############################################################################


def unique_nodes(
    nodes: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Remove duplicate nodes by id.
    """

    seen: dict[str, dict[str, Any]] = {}

    for node in nodes:
        if validate_node(node):
            seen[node["id"]] = node

    return list(seen.values())


###############################################################################


def unique_edges(
    edges: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Remove duplicate edges.
    """

    seen: dict[
        tuple[str, str, str],
        dict[str, Any],
    ] = {}

    for edge in edges:
        if validate_edge(edge):
            key = (
                edge["source"],
                edge["target"],
                edge["relationship"],
            )
            seen[key] = edge

    return list(seen.values())