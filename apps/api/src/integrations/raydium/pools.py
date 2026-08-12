"""
Raydium Pool Manager
====================

Pool analytics and management layer for Sentinel AI.
"""

###############################################################################
# Imports
###############################################################################

from __future__ import annotations

from typing import Dict, List

###############################################################################
# PoolManager
###############################################################################


class PoolManager:
    """
    Handles Raydium liquidity pool operations.
    """

    ###########################################################################
    # Pool Management
    ###########################################################################

    def pool(
        self,
        data: Dict,
    ) -> Dict:

        return normalize_pool(data)

    ###########################################################################

    def pools(
        self,
        data: List[Dict],
    ) -> List[Dict]:

        return [
            normalize_pool(pool)
            for pool in data
        ]

    ###########################################################################

    def pool_statistics(
        self,
        pool: Dict,
    ) -> Dict:

        return {
            "price": self.pool_price(pool),
            "liquidity": self.pool_liquidity(pool),
            "volume": self.pool_volume(pool),
            "apr": self.pool_apr(pool),
            "fee": self.pool_fee(pool),
        }

    ###########################################################################

    def pool_liquidity(
        self,
        pool: Dict,
    ) -> float:

        return float(
            pool.get("liquidity", 0)
        )

    ###########################################################################

    def pool_volume(
        self,
        pool: Dict,
    ) -> float:

        return float(
            pool.get("volume24h", 0)
        )

    ###########################################################################

    def pool_price(
        self,
        pool: Dict,
    ) -> float:

        return float(
            pool.get("price", 0)
        )

    ###########################################################################

    def pool_apr(
        self,
        pool: Dict,
    ) -> float:

        return float(
            pool.get("apr", 0)
        )

    ###########################################################################

    def pool_fee(
        self,
        pool: Dict,
    ) -> float:

        return float(
            pool.get("fee", 0)
        )

    ###########################################################################

    def pool_score(
        self,
        pool: Dict,
    ) -> float:

        liquidity = self.pool_liquidity(pool)

        volume = self.pool_volume(pool)

        apr = self.pool_apr(pool)

        score = (
            liquidity * 0.40
            + volume * 0.40
            + apr * 0.20
        )

        return round(score, 2)

    ###########################################################################
    # Runtime
    ###########################################################################

    def summary(self):

        return {
            "manager": "PoolManager",
            "provider": "Raydium",
        }


###############################################################################
# Utilities
###############################################################################


def normalize_pool(
    pool: Dict,
) -> Dict:

    return {
        "pool_id": pool.get("id"),
        "base_mint": pool.get("baseMint"),
        "quote_mint": pool.get("quoteMint"),
        "price": pool.get("price"),
        "liquidity": pool.get("liquidity"),
        "volume24h": pool.get("volume24h"),
        "apr": pool.get("apr"),
        "fee": pool.get("fee"),
    }


###############################################################################


def pool_metadata(
    pool: Dict,
) -> Dict:

    return {
        "pool_id": pool.get("id"),
        "base_mint": pool.get("baseMint"),
        "quote_mint": pool.get("quoteMint"),
    }