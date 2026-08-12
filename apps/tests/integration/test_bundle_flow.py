"""
Bundle flow integration tests.
"""

from __future__ import annotations

import unittest


class BundleFlowTests(unittest.TestCase):

    def setUp(self):
        self.bundle = self.mock_bundle()

    def tearDown(self):
        self.bundle = None

    # Bundle

    def test_bundle_detection(self): ...
    def test_bundle_database(self): ...
    def test_bundle_graph(self): ...
    def test_bundle_score(self): ...

    # Relationships

    def test_bundle_wallets(self): ...
    def test_bundle_deployer(self): ...

    # Runtime

    def diagnostics(self): ...
    def summary(self): ...

    def mock_bundle(self):
        return {}


if __name__ == "__main__":
    unittest.main()