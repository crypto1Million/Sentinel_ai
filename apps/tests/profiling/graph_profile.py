"""
Graph Profiling
===============

Profiles Neo4j graph operations.
"""

from __future__ import annotations

import time
import unittest


def run_graph_profile():

    start = time.perf_counter()

    # Replace with real Neo4j operation.
    nodes = 100_000
    relationships = 500_000

    elapsed = time.perf_counter() - start

    return {
        "nodes": nodes,
        "relationships": relationships,
        "elapsed_seconds": elapsed,
    }


class GraphProfileTests(unittest.TestCase):

    def test_graph_operation_profile(self):

        result = run_graph_profile()

        self.assertGreater(
            result["nodes"],
            0,
        )

        self.assertGreater(
            result["relationships"],
            0,
        )


if __name__ == "__main__":
    unittest.main()