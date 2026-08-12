"""
Graph flow integration tests.
"""

from __future__ import annotations

import unittest


class GraphFlowTests(unittest.TestCase):

    def setUp(self):
        self.graph = self.mock_graph()

    def tearDown(self):
        self.graph = None

    # Nodes

    def test_wallet_nodes(self): ...
    def test_token_nodes(self): ...
    def test_bundle_nodes(self): ...

    # Relationships

    def test_transfer_edges(self): ...
    def test_funding_edges(self): ...
    def test_holder_edges(self): ...

    # Analytics

    def test_graph_clusters(self): ...
    def test_shortest_path(self): ...
    def test_pagerank(self): ...

    # Runtime

    def diagnostics(self): ...
    def summary(self): ...

    def mock_graph(self):
        return {}


if __name__ == "__main__":
    unittest.main()