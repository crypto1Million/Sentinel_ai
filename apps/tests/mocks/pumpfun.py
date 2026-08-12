"""
Mock Pump.fun Integration
=========================

Fake Pump.fun token-launch provider used by Sentinel AI tests.
"""

from __future__ import annotations

from typing import Any, Dict, List


class MockPumpFun:

    def __init__(self):

        self.tokens: Dict[str, Dict[str, Any]] = {}

        self.launches: List[Dict[str, Any]] = []

    # ------------------------------------------------------------------
    # Token Launch
    # ------------------------------------------------------------------

    def create_token(
        self,
        mint: str,
        name: str,
        symbol: str,
        creator: str,
        initial_liquidity: float = 20.0,
    ):

        token = {
            "mint": mint,
            "name": name,
            "symbol": symbol,
            "creator": creator,
            "initial_liquidity": initial_liquidity,
            "bonding_curve": True,
        }

        self.tokens[mint] = token
        self.launches.append(token)

        return token

    # ------------------------------------------------------------------
    # Token Lookup
    # ------------------------------------------------------------------

    def get_token(
        self,
        mint: str,
    ):

        return self.tokens.get(mint)

    # ------------------------------------------------------------------
    # Launch Detection
    # ------------------------------------------------------------------

    def get_launches(self):

        return list(self.launches)

    def latest_launch(self):

        if not self.launches:
            return None

        return self.launches[-1]

    # ------------------------------------------------------------------
    # Runtime
    # ------------------------------------------------------------------

    def diagnostics(self):

        return {
            "connected": True,
            "tokens": len(self.tokens),
            "launches": len(self.launches),
        }

    def summary(self):

        return {
            "service": "mock-pumpfun",
            "tokens": len(self.tokens),
            "launches": len(self.launches),
        }


# ----------------------------------------------------------------------
# Factory
# ----------------------------------------------------------------------

def mock_pumpfun() -> MockPumpFun:

    pumpfun = MockPumpFun()

    pumpfun.create_token(
        mint="TOKEN001",
        name="Test Meme",
        symbol="TMEME",
        creator="Wallet001",
        initial_liquidity=20.0,
    )

    pumpfun.create_token(
        mint="TOKEN002",
        name="AI Dog",
        symbol="AIDOG",
        creator="Wallet002",
        initial_liquidity=15.0,
    )

    return pumpfun