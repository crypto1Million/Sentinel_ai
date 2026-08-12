"""
Neo4j Utilities
===============
"""

from __future__ import annotations

from typing import Dict, List


###############################################################################
# Labels
###############################################################################


def node_label(name: str):

    return name.replace(" ", "_")


###############################################################################


def relationship_name(name: str):

    return (
        name.upper()
        .replace(" ", "_")
    )


###############################################################################
# Properties
###############################################################################


def clean_properties(
    properties: Dict,
):

    return {
        k: v
        for k, v in properties.items()
        if v is not None
    }


###############################################################################


def merge_properties(
    base: Dict,
    update: Dict,
):

    merged = dict(base)

    merged.update(update)

    return merged


###############################################################################
# Query
###############################################################################


def normalize_query(
    query: str,
):

    return " ".join(
        query.split()
    )


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
# Graph
###############################################################################


def unique_addresses(
    addresses: List[str],
):

    return list(
        dict.fromkeys(addresses)
    )


###############################################################################


def chunk_list(
    items: List,
    size: int,
):

    for i in range(
        0,
        len(items),
        size,
    ):

        yield items[i : i + size]


###############################################################################
# Runtime
###############################################################################


def diagnostics():

    return {
        "utilities": "loaded",
    }


###############################################################################


def summary():

    return {
        "module": "neo4j.utils",
    }


###############################################################################
# Metadata
###############################################################################


def utility_metadata():

    return {
        "provider": "Neo4j",
        "version": "1.0.0",
    }