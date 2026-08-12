###############################################################################
# Imports
###############################################################################

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

###############################################################################
# Base Model
###############################################################################


class GraphBase(BaseModel):
    """
    Base graph model.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )


###############################################################################
# Node
###############################################################################


class Node(GraphBase):
    id: str
    label: str
    type: str
    score: float | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


###############################################################################
# Edge
###############################################################################


class Edge(GraphBase):
    source: str
    target: str
    relationship: str
    weight: float = 1.0
    metadata: dict[str, Any] = Field(default_factory=dict)


###############################################################################
# Graph
###############################################################################


class Graph(GraphBase):
    nodes: list[Node] = Field(default_factory=list)
    edges: list[Edge] = Field(default_factory=list)


###############################################################################
# GraphStatistics
###############################################################################


class GraphStatistics(GraphBase):
    node_count: int
    edge_count: int
    cluster_count: int
    connected_components: int
    density: float
    average_degree: float
    generated_at: datetime


###############################################################################
# GraphResponse
###############################################################################


class GraphResponse(GraphBase):
    graph: Graph
    statistics: GraphStatistics
    metadata: "GraphMetadata"


###############################################################################
# GraphMetadata
###############################################################################


class GraphMetadata(GraphBase):
    graph_id: str
    generated_at: datetime
    query: str | None = None
    source: str | None = None
    version: str = "1.0.0"


###############################################################################
# Utilities
###############################################################################


def graph_summary(
    graph: Graph,
) -> dict[str, Any]:
    """
    Serialize graph.
    """

    return graph.model_dump()


###############################################################################


def empty_graph() -> Graph:
    """
    Create empty graph.
    """

    return Graph()