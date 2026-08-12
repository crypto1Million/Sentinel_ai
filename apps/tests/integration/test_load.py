"""
Load Integration Tests
======================
"""

from __future__ import annotations

import unittest


class LoadTests(unittest.TestCase):

    def setUp(self):
        self.system = self.mock_system()

    def tearDown(self):
        self.system = None

    # Load

    def test_100_requests(self): ...
    def test_1000_requests(self): ...
    def test_parallel_users(self): ...
    def test_parallel_workers(self): ...
    def test_parallel_swaps(self): ...

    # Runtime

    def diagnostics(self): ...
    def summary(self): ...

    def mock_system(self):
        return {}


if __name__ == "__main__":
    unittest.main()