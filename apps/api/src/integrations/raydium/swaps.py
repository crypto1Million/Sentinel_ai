"""
Raydium Swap Manager
====================

Handles swap execution, simulation and analytics.
"""

###############################################################################
# Imports
###############################################################################

from __future__ import annotations

from typing import Dict, List

###############################################################################
# SwapManager
###############################################################################


class SwapManager:
    """
    Raydium Swap Manager.
    """

    ###########################################################################
    # Swaps
    ###########################################################################

    def quote(
        self,
        quote_data: Dict,
    ) -> Dict:

        return normalize_swap(
            quote_data
        )

    ###########################################################################

    def build_transaction(
        self,
        swap: Dict,
    ) -> Dict:

        return {
            "instruction": "swap",
            "payload": normalize_swap(
                swap
            ),
        }

    ###########################################################################

    def simulate(
        self,
        swap: Dict,
    ) -> Dict:

        return {
            "success": True,
            "estimated_output": swap.get(
                "output_amount",
                0,
            ),
            "price_impact": swap.get(
                "price_impact",
                0,
            ),
        }

    ###########################################################################

    def execute(
        self,
        swap: Dict,
    ) -> Dict:

        return {
            "status": "submitted",
            "signature": swap.get(
                "signature",
            ),
        }

    ###########################################################################

    def swap_history(
        self,
        swaps: List[Dict],
    ) -> List[Dict]:

        return [
            normalize_swap(i)
            for i in swaps
        ]

    ###########################################################################

    def swap_statistics(
        self,
        swaps: List[Dict],
    ) -> Dict:

        total_volume = sum(
            float(
                swap.get(
                    "input_amount",
                    0,
                )
            )
            for swap in swaps
        )

        return {
            "total_swaps": len(swaps),
            "total_volume": total_volume,
        }

    ###########################################################################

    def swap_score(
        self,
        swap: Dict,
    ) -> float:

        impact = float(
            swap.get(
                "price_impact",
                0,
            )
        )

        liquidity = float(
            swap.get(
                "liquidity",
                0,
            )
        )

        score = max(
            0.0,
            100 - impact * 10,
        )

        if liquidity > 0:

            score += 5

        return round(
            min(score, 100),
            2,
        )

    ###########################################################################
    # Runtime
    ###########################################################################

    def summary(self):

        return {
            "manager": "SwapManager",
            "provider": "Raydium",
        }


###############################################################################
# Utilities
###############################################################################


def normalize_swap(
    swap: Dict,
) -> Dict:

    return {
        "input_token": swap.get(
            "input_token",
        ),
        "output_token": swap.get(
            "output_token",
        ),
        "input_amount": swap.get(
            "input_amount",
        ),
        "output_amount": swap.get(
            "output_amount",
        ),
        "price_impact": swap.get(
            "price_impact",
        ),
        "minimum_received": swap.get(
            "minimum_received",
        ),
        "signature": swap.get(
            "signature",
        ),
        "liquidity": swap.get(
            "liquidity",
        ),
    }


###############################################################################


def swap_metadata(
    swap: Dict,
) -> Dict:

    return {
        "signature": swap.get(
            "signature",
        ),
        "input_token": swap.get(
            "input_token",
        ),
        "output_token": swap.get(
            "output_token",
        ),
    }