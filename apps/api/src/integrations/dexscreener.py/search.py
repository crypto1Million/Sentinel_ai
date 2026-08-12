"""
DexScreener Search Manager
==========================

Search and filtering utilities for DexScreener.
"""

###############################################################################
# Imports
###############################################################################

from __future__ import annotations

from typing import Dict, List

###############################################################################
# SearchManager
###############################################################################


class SearchManager:
    """
    Handles searching and filtering of DexScreener pairs.
    """

    ###########################################################################
    # Search
    ###########################################################################

    def search(
        self,
        query: str,
        pairs: List[Dict],
    ) -> List[Dict]:

        query = query.lower()

        return [
            pair
            for pair in pairs
            if query in str(pair).lower()
        ]

    ###########################################################################

    def search_symbol(
        self,
        symbol: str,
        pairs: List[Dict],
    ) -> List[Dict]:

        symbol = symbol.lower()

        return [
            pair
            for pair in pairs
            if pair.get("base_token", {})
            .get("symbol", "")
            .lower()
            == symbol
        ]

    ###########################################################################

    def search_name(
        self,
        name: str,
        pairs: List[Dict],
    ) -> List[Dict]:

        name = name.lower()

        return [
            pair
            for pair in pairs
            if name in pair.get("base_token", {})
            .get("name", "")
            .lower()
        ]

    ###########################################################################

    def search_pair(
        self,
        pair_address: str,
        pairs: List[Dict],
    ) -> Dict | None:

        for pair in pairs:

            if (
                pair.get("pair_address")
                == pair_address
            ):

                return pair

        return None

    ###########################################################################

    def search_chain(
        self,
        chain: str,
        pairs: List[Dict],
    ) -> List[Dict]:

        chain = chain.lower()

        return [
            pair
            for pair in pairs
            if pair.get("chain", "")
            .lower()
            == chain
        ]

    ###########################################################################

    def autocomplete(
        self,
        prefix: str,
        pairs: List[Dict],
    ) -> List[str]:

        prefix = prefix.lower()

        results = []

        for pair in pairs:

            symbol = (
                pair.get("base_token", {})
                .get("symbol", "")
            )

            if symbol.lower().startswith(prefix):

                results.append(symbol)

        return sorted(
            list(set(results))
        )

    ###########################################################################
    # Filters
    ###########################################################################

    def by_volume(
        self,
        pairs: List[Dict],
        minimum: float,
    ) -> List[Dict]:

        return [
            pair
            for pair in pairs
            if pair.get("volume", 0)
            >= minimum
        ]

    ###########################################################################

    def by_liquidity(
        self,
        pairs: List[Dict],
        minimum: float,
    ) -> List[Dict]:

        return [
            pair
            for pair in pairs
            if pair.get("liquidity", 0)
            >= minimum
        ]

    ###########################################################################

    def by_marketcap(
        self,
        pairs: List[Dict],
        minimum: float,
        maximum: float,
    ) -> List[Dict]:

        return [
            pair
            for pair in pairs
            if minimum
            <= pair.get("marketCap", 0)
            <= maximum
        ]

    ###########################################################################

    def by_age(
        self,
        pairs: List[Dict],
        maximum_age_hours: int,
    ) -> List[Dict]:

        return [
            pair
            for pair in pairs
            if pair.get("ageHours", 0)
            <= maximum_age_hours
        ]

    ###########################################################################

    def verified(
        self,
        pairs: List[Dict],
    ) -> List[Dict]:

        return [
            pair
            for pair in pairs
            if pair.get("verified", False)
        ]

    ###########################################################################
    # Runtime
    ###########################################################################

    def summary(self):

        return {
            "manager": "SearchManager",
            "provider": "DexScreener",
        }


###############################################################################
# Utilities
###############################################################################


def normalize_search(
    query: str,
) -> str:

    return query.strip().lower()


###############################################################################


def metadata():

    return {
        "search_engine": "DexScreener",
        "supports": [
            "symbol",
            "name",
            "pair",
            "chain",
            "autocomplete",
        ],
    }