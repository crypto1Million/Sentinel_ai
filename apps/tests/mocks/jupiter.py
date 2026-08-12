"""
Mock Jupiter Integration
========================

Fake Jupiter quotes, routes and swap execution.
"""

from __future__ import annotations

from typing import Any, Dict, List


class MockJupiter:

    def __init__(self):

        self.swaps: List[Dict[str, Any]] = []

    # ------------------------------------------------------------------
    # Quotes
    # ------------------------------------------------------------------

    def quote(
        self,
        input_mint: str,
        output_mint: str,
        amount: float,
    ):

        return {
            "input_mint": input_mint,
            "output_mint": output_mint,
            "input_amount": amount,
            "output_amount": amount * 0.98,
            "price_impact": 0.004,
            "route": [
                "SOL",
                output_mint,
            ],
        }

    # ------------------------------------------------------------------
    # Routes
    # ------------------------------------------------------------------

    def route(
        self,
        input_mint: str,
        output_mint: str,
        amount: float,
    ):

        return {
            "input_mint": input_mint,
            "output_mint": output_mint,
            "amount": amount,
            "route": [
                {
                    "dex": "Raydium",
                    "input": input_mint,
                    "output": output_mint,
                }
            ],
        }

    # ------------------------------------------------------------------
    # Swap
    # ------------------------------------------------------------------

    def swap(
        self,
        input_mint: str,
        output_mint: str,
        amount: float,
        slippage_bps: int = 100,
    ):

        result = {
            "input_mint": input_mint,
            "output_mint": output_mint,
            "amount": amount,
            "slippage_bps": slippage_bps,
            "success": True,
            "signature": f"MOCK_SWAP_{len(self.swaps) + 1}",
        }

        self.swaps.append(result)

        return result

    # ------------------------------------------------------------------
    # Runtime
    # ------------------------------------------------------------------

    def diagnostics(self):

        return {
            "connected": True,
            "swaps": len(self.swaps),
        }

    def summary(self):

        return {
            "service": "mock-jupiter",
            "swaps": len(self.swaps),
        }


def mock_jupiter() -> MockJupiter:

    return MockJupiter()