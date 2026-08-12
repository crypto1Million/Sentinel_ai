"""
Raydium Parser
==============

Parser for Raydium API responses into Sentinel AI normalized structures.
"""

###############################################################################
# Imports
###############################################################################

from __future__ import annotations

from typing import Any, Dict, List


###############################################################################
# RaydiumParser
###############################################################################


class RaydiumParser:
    """
    Parser for Raydium objects.
    """

    ###########################################################################
    # Pool
    ###########################################################################

    def parse_pool(
        self,
        data: Dict,
    ) -> Dict:

        return normalize(
            {
                "pool_id": data.get("id"),
                "base_token": self.parse_token(
                    data.get("baseToken", {})
                ),
                "quote_token": self.parse_token(
                    data.get("quoteToken", {})
                ),
                "liquidity": self.parse_liquidity(data),
                "apr": self.parse_apr(data),
                "fee": self.parse_fee(data),
                "volume": self.parse_volume(data),
                "metadata": self.parse_metadata(data),
            }
        )

    ###########################################################################
    # Token
    ###########################################################################

    def parse_token(
        self,
        data: Dict,
    ) -> Dict:

        return normalize(
            {
                "mint": data.get("mint"),
                "symbol": data.get("symbol"),
                "name": data.get("name"),
                "decimals": data.get("decimals"),
            }
        )

    ###########################################################################
    # Swap
    ###########################################################################

    def parse_swap(
        self,
        data: Dict,
    ) -> Dict:

        return normalize(
            {
                "input_token": data.get("inputToken"),
                "output_token": data.get("outputToken"),
                "input_amount": data.get("inputAmount"),
                "output_amount": data.get("outputAmount"),
                "price_impact": data.get("priceImpact"),
                "minimum_received": data.get(
                    "minimumReceived"
                ),
            }
        )

    ###########################################################################
    # Liquidity
    ###########################################################################

    def parse_liquidity(
        self,
        data: Dict,
    ) -> Dict:

        return normalize(
            {
                "usd": data.get("liquidity"),
                "base": data.get("baseReserve"),
                "quote": data.get("quoteReserve"),
                "lp_supply": data.get("lpSupply"),
            }
        )

    ###########################################################################
    # APR
    ###########################################################################

    def parse_apr(
        self,
        data: Dict,
    ) -> Dict:

        return normalize(
            {
                "apr": data.get("apr"),
                "farm_apr": data.get("farmApr"),
            }
        )

    ###########################################################################
    # Fee
    ###########################################################################

    def parse_fee(
        self,
        data: Dict,
    ) -> Dict:

        return normalize(
            {
                "swap_fee": data.get("fee"),
                "protocol_fee": data.get(
                    "protocolFee"
                ),
            }
        )

    ###########################################################################
    # Volume
    ###########################################################################

    def parse_volume(
        self,
        data: Dict,
    ) -> Dict:

        return normalize(
            {
                "24h": data.get("volume24h"),
                "7d": data.get("volume7d"),
                "30d": data.get("volume30d"),
            }
        )

    ###########################################################################
    # Metadata
    ###########################################################################

    def parse_metadata(
        self,
        data: Dict,
    ) -> Dict:

        return normalize(
            {
                "created_at": data.get(
                    "createdAt"
                ),
                "status": data.get("status"),
                "program": data.get("programId"),
                "authority": data.get(
                    "authority"
                ),
            }
        )

    ###########################################################################
    # Runtime
    ###########################################################################

    def diagnostics(
        self,
    ) -> Dict:

        return {
            "parser": "RaydiumParser",
            "status": "healthy",
        }

    ###########################################################################

    def summary(
        self,
    ) -> Dict:

        return {
            "supported": [
                "pool",
                "token",
                "swap",
                "liquidity",
                "apr",
                "fee",
                "volume",
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
        key: value
        for key, value in data.items()
        if value is not None
    }


###############################################################################


def extract_addresses(
    data: Dict,
) -> List[str]:

    addresses = []

    for value in data.values():

        if isinstance(value, dict):

            mint = value.get("mint")

            if mint:

                addresses.append(mint)

        elif isinstance(value, str):

            if len(value) > 30:

                addresses.append(value)

    return list(set(addresses))