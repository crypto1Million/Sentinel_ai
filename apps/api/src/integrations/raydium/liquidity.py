"""
Raydium Liquidity Manager
=========================

Liquidity management layer for Raydium pools.
"""

###############################################################################
# Imports
###############################################################################

from __future__ import annotations

from typing import Dict, List

###############################################################################
# LiquidityManager
###############################################################################


class LiquidityManager:
    """
    Handles LP positions and liquidity analytics.
    """

    ###########################################################################
    # Liquidity
    ###########################################################################

    def add_liquidity(
        self,
        pool: Dict,
        amount_a: float,
        amount_b: float,
    ) -> Dict:

        return {
            "status": "success",
            "pool": pool.get("id"),
            "amount_a": amount_a,
            "amount_b": amount_b,
        }

    ###########################################################################

    def remove_liquidity(
        self,
        pool: Dict,
        percentage: float,
    ) -> Dict:

        return {
            "status": "success",
            "pool": pool.get("id"),
            "removed": percentage,
        }

    ###########################################################################

    def liquidity_position(
        self,
        position: Dict,
    ) -> Dict:

        return normalize_liquidity(position)

    ###########################################################################

    def liquidity_statistics(
        self,
        positions: List[Dict],
    ) -> Dict:

        total = sum(
            float(
                position.get(
                    "usd_value",
                    0,
                )
            )
            for position in positions
        )

        return {
            "positions": len(positions),
            "total_value": total,
        }

    ###########################################################################

    def pool_depth(
        self,
        pool: Dict,
    ) -> Dict:

        return {
            "base": pool.get("base_reserve"),
            "quote": pool.get("quote_reserve"),
        }

    ###########################################################################

    def lp_tokens(
        self,
        pool: Dict,
    ) -> float:

        return float(
            pool.get(
                "lp_supply",
                0,
            )
        )

    ###########################################################################

    def lp_score(
        self,
        pool: Dict,
    ) -> float:

        liquidity = float(
            pool.get(
                "liquidity",
                0,
            )
        )

        score = min(
            liquidity / 10000,
            100,
        )

        return round(score, 2)

    ###########################################################################
    # Runtime
    ###########################################################################

    def summary(self):

        return {
            "manager": "LiquidityManager",
            "provider": "Raydium",
        }


###############################################################################
# Utilities
###############################################################################


def normalize_liquidity(
    position: Dict,
) -> Dict:

    return {
        "pool": position.get("pool"),
        "lp_tokens": position.get("lp_tokens"),
        "usd_value": position.get("usd_value"),
        "share": position.get("share"),
        "base_amount": position.get("base_amount"),
        "quote_amount": position.get("quote_amount"),
    }


###############################################################################


def liquidity_metadata(
    position: Dict,
) -> Dict:

    return {
        "pool": position.get("pool"),
        "lp_tokens": position.get("lp_tokens"),
    }