"""
Mock Raydium Integration
========================

Fake Raydium pools, liquidity and swap execution.
"""

from __future__ import annotations

from typing import Any, Dict, List


class MockRaydium:

    def __init__(self):

        self.pools: Dict[str, Dict[str, Any]] = {}

        self.swaps: List[Dict[str, Any]] = []

    # ------------------------------------------------------------------
    # Pools
    # ------------------------------------------------------------------

    def create_pool(
        self,
        pool_id: str,
        token_a: str,
        token_b: str,
        liquidity: float,
    ):

        pool = {
            "pool_id": pool_id,
            "token_a": token_a,
            "token_b": token_b,
            "liquidity": liquidity,
        }

        self.pools[pool_id] = pool

        return pool

    def get_pool(
        self,
        pool_id: str,
    ):

        return self.pools.get(pool_id)

    def get_liquidity(
        self,
        pool_id: str,
    ):

        pool = self.get_pool(pool_id)

        if not pool:
            return 0.0

        return pool["liquidity"]

    # ------------------------------------------------------------------
    # Swaps
    # ------------------------------------------------------------------

    def swap(
        self,
        pool_id: str,
        token_in: str,
        token_out: str,
        amount: float,
        slippage: float = 0.01,
    ):

        pool = self.get_pool(pool_id)

        if not pool:
            raise ValueError("Pool not found")

        output_amount = amount * 0.98

        result = {
            "pool_id": pool_id,
            "token_in": token_in,
            "token_out": token_out,
            "input_amount": amount,
            "output_amount": output_amount,
            "slippage": slippage,
            "success": True,
        }

        self.swaps.append(result)

        return result

    # ------------------------------------------------------------------
    # Runtime
    # ------------------------------------------------------------------

    def diagnostics(self):

        return {
            "connected": True,
            "pools": len(self.pools),
            "swaps": len(self.swaps),
        }

    def summary(self):

        return {
            "service": "mock-raydium",
            "pools": len(self.pools),
            "swaps": len(self.swaps),
        }


def mock_raydium() -> MockRaydium:

    raydium = MockRaydium()

    raydium.create_pool(
        pool_id="POOL001",
        token_a="SOL",
        token_b="TOKEN001",
        liquidity=250_000,
    )

    raydium.create_pool(
        pool_id="POOL002",
        token_a="SOL",
        token_b="TOKEN002",
        liquidity=50_000,
    )

    return raydium