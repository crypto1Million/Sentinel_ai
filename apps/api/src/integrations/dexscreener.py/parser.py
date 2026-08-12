"""
DexScreener Parser
==================

Parses DexScreener API responses into normalized Sentinel AI models.
"""

###############################################################################
# Imports
###############################################################################

from __future__ import annotations

from typing import Any, Dict, List

###############################################################################
# Pair Parser
###############################################################################


class DexParser:
    """
    Parser for DexScreener responses.
    """

    ###########################################################################

    def parse_pair(
        self,
        data: Dict,
    ) -> Dict:

        return normalize(
            {
                "pair_address": data.get("pairAddress"),
                "chain": data.get("chainId"),
                "dex": data.get("dexId"),
                "base_token": self.parse_token(
                    data.get("baseToken", {})
                ),
                "quote_token": self.parse_token(
                    data.get("quoteToken", {})
                ),
                "price": self.parse_price(data),
                "liquidity": self.parse_liquidity(data),
                "volume": self.parse_volume(data),
                "transactions": self.parse_transactions(data),
                "holders": self.parse_holders(data),
                "metadata": self.parse_metadata(data),
            }
        )

    ###########################################################################

    def parse_token(
        self,
        data: Dict,
    ) -> Dict:

        return normalize(
            {
                "address": data.get("address"),
                "name": data.get("name"),
                "symbol": data.get("symbol"),
            }
        )

    ###########################################################################

    def parse_price(
        self,
        data: Dict,
    ) -> Dict:

        return normalize(
            {
                "usd": data.get("priceUsd"),
                "native": data.get("priceNative"),
            }
        )

    ###########################################################################

    def parse_liquidity(
        self,
        data: Dict,
    ) -> Dict:

        liquidity = data.get(
            "liquidity",
            {},
        )

        return normalize(
            {
                "usd": liquidity.get("usd"),
                "base": liquidity.get("base"),
                "quote": liquidity.get("quote"),
            }
        )

    ###########################################################################

    def parse_volume(
        self,
        data: Dict,
    ) -> Dict:

        return normalize(
            data.get(
                "volume",
                {},
            )
        )

    ###########################################################################

    def parse_transactions(
        self,
        data: Dict,
    ) -> Dict:

        return normalize(
            data.get(
                "txns",
                {},
            )
        )

    ###########################################################################

    def parse_holders(
        self,
        data: Dict,
    ) -> List[Dict]:

        return data.get(
            "holders",
            [],
        )

    ###########################################################################

    def parse_metadata(
        self,
        data: Dict,
    ) -> Dict:

        return normalize(
            {
                "fdv": data.get("fdv"),
                "market_cap": data.get("marketCap"),
                "labels": data.get("labels"),
                "pair_created": data.get(
                    "pairCreatedAt"
                ),
                "url": data.get("url"),
            }
        )

    ###########################################################################
    # Runtime
    ###########################################################################

    def diagnostics(self):

        return {
            "parser": "DexParser",
            "status": "healthy",
        }

    ###########################################################################

    def summary(self):

        return {
            "supported": [
                "pair",
                "token",
                "price",
                "liquidity",
                "volume",
                "transactions",
                "holders",
                "metadata",
            ]
        }


###############################################################################
# Utilities
###############################################################################


def normalize(
    data: Dict,
) -> Dict:

    return {
        k: v
        for k, v in data.items()
        if v is not None
    }


###############################################################################


def extract_addresses(
    pair: Dict,
) -> List[str]:

    addresses = []

    base = (
        pair.get("baseToken", {})
        .get("address")
    )

    quote = (
        pair.get("quoteToken", {})
        .get("address")
    )

    if base:

        addresses.append(base)

    if quote:

        addresses.append(quote)

    return list(set(addresses))