"""
Trading Flow Integration Tests
==============================
"""

from __future__ import annotations

import unittest


class TradingFlowTests(unittest.TestCase):

    def setUp(self):
        self.trade = self.mock_trade()

    def tearDown(self):
        self.trade = None

    # Trading Flow

    def test_quote_to_swap(self): ...
    def test_swap_execution(self): ...
    def test_order_flow(self): ...
    def test_position_update(self): ...
    def test_portfolio_sync(self): ...

    # Runtime

    def diagnostics(self): ...
    def summary(self): ...

    def mock_trade(self):
        return {}


if __name__ == "__main__":
    unittest.main()