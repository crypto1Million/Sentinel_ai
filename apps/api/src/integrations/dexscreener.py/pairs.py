"""
DexScreener Pair Manager
========================

Handles pair-level operations and analytics.
"""

###############################################################################
# Imports
###############################################################################

from __future__ import annotations

from typing import Dict, List

###############################################################################
# PairManager
###############################################################################


class PairManager:
    """
    Pair Management Layer.
    """

    ###########################################################################
    # Pair Management
    ###########################################################################

    def pair(
        self,
        data: Dict,
    ) -> Dict:

        return normalize_pair(data)

    ###########################################################################

    def pairs(
        self,
        items: List[Dict],
    ) -> List[Dict]:

        return [
            normalize_pair(item)
            for item in items
        ]

    ###########################################################################

    def pair_statistics(
        self,
        pair: Dict,
    ) -> Dict:

        return {
            "price": pair.get("priceUsd"),
            "liquidity": pair.get("liquidity"),
            "volume": pair.get("volume"),
            "market_cap": pair.get("marketCap"),
            "fdv": pair.get("fdv"),
        }

    ###########################################################################

    def pair_liquidity(
        self,
        pair: Dict,
    ) -> float:

        return float(
            pair.get("liquidity", 0)
        )

    ###########################################################################

    def pair_volume(
        self,
        pair: Dict,
    ) -> float:

        return float(
            pair.get("volume", 0)
        )

    ###########################################################################

    def pair_price(
        self,
        pair: Dict,
    ) -> float:

        return float(
            pair.get("priceUsd", 0)
        )

    ###########################################################################

    def pair_holders(
        self,
        pair: Dict,
    ) -> List:

        return pair.get(
            "holders",
            [],
        )

    ###########################################################################

    def pair_transactions(
        self,
        pair: Dict,
    ) -> Dict:

        return pair.get(
            "txns",
            {},
        )

    ###########################################################################

    def pair_score(
        self,
        pair: Dict,
    ) -> float:

        liquidity = float(
            pair.get("liquidity", 0)
        )

        volume = float(
            pair.get("volume", 0)
        )

        score = (
            liquidity * 0.5
            + volume * 0.5
        )

        return round(score, 2)

    ###########################################################################
    # Runtime
    ###########################################################################

    def summary(self):

        return {
            "manager": "PairManager",
            "provider": "DexScreener",
        }


###############################################################################
# Utilities
###############################################################################


def normalize_pair(
    pair: Dict,
) -> Dict:

    return {
        "pair_address": pair.get("pairAddress"),
        "chain": pair.get("chainId"),
        "dex": pair.get("dexId"),
        "base_token": pair.get("baseToken"),
        "quote_token": pair.get("quoteToken"),
        "priceUsd": pair.get("priceUsd"),
        "liquidity": pair.get("liquidity"),
        "volume": pair.get("volume"),
        "marketCap": pair.get("marketCap"),
        "fdv": pair.get("fdv"),
        "txns": pair.get("txns"),
    }


###############################################################################


def pair_metadata(
    pair: Dict,
) -> Dict:

    return {
        "pair": pair.get("pairAddress"),
        "chain": pair.get("chainId"),
        "dex": pair.get("dexId"),
    }