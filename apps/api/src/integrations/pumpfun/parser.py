"""
Pump.fun Parser
===============

Parses Pump.fun API responses into normalized Sentinel AI models.
"""

###############################################################################
# Imports
###############################################################################

from __future__ import annotations

from typing import Any, Dict, List

###############################################################################
# Token Parser
###############################################################################


class PumpFunParser:
    """
    Parser for Pump.fun API responses.
    """

    ###########################################################################

    def parse_token(
        self,
        data: Dict,
    ) -> Dict:

        return normalize(
            {
                "mint": data.get("mint"),
                "name": data.get("name"),
                "symbol": data.get("symbol"),
                "market_cap": data.get("marketCap"),
                "creator": data.get("creator"),
                "created_at": data.get("createdAt"),
            }
        )

    ###########################################################################

    def parse_deployer(
        self,
        data: Dict,
    ) -> Dict:

        return normalize(
            {
                "wallet": data.get("creator"),
                "token_count": data.get("tokenCount"),
                "successful_launches": data.get("successfulLaunches"),
            }
        )

    ###########################################################################

    def parse_bonding_curve(
        self,
        data: Dict,
    ) -> Dict:

        return normalize(
            {
                "progress": data.get("progress"),
                "virtual_sol": data.get("virtualSolReserves"),
                "virtual_token": data.get("virtualTokenReserves"),
            }
        )

    ###########################################################################

    def parse_liquidity(
        self,
        data: Dict,
    ) -> Dict:

        return normalize(
            {
                "liquidity": data.get("liquidity"),
                "volume": data.get("volume"),
                "price": data.get("price"),
            }
        )

    ###########################################################################

    def parse_migration(
        self,
        data: Dict,
    ) -> Dict:

        return normalize(
            {
                "migrated": data.get("migrated"),
                "migration_time": data.get("migrationTime"),
                "destination": data.get("destination"),
            }
        )

    ###########################################################################

    def parse_holders(
        self,
        holders: List[Dict],
    ) -> List[Dict]:

        return [
            normalize(
                {
                    "wallet": holder.get("wallet"),
                    "balance": holder.get("balance"),
                    "percentage": holder.get("percentage"),
                }
            )
            for holder in holders
        ]

    ###########################################################################

    def parse_transactions(
        self,
        transactions: List[Dict],
    ) -> List[Dict]:

        return [
            normalize(
                {
                    "signature": tx.get("signature"),
                    "wallet": tx.get("wallet"),
                    "amount": tx.get("amount"),
                    "side": tx.get("side"),
                    "timestamp": tx.get("timestamp"),
                }
            )
            for tx in transactions
        ]

    ###########################################################################

    def parse_metadata(
        self,
        data: Dict,
    ) -> Dict:

        return normalize(
            {
                "website": data.get("website"),
                "telegram": data.get("telegram"),
                "twitter": data.get("twitter"),
                "description": data.get("description"),
            }
        )

    ###########################################################################
    # Runtime
    ###########################################################################

    def diagnostics(self):

        return {
            "parser": "PumpFunParser",
            "status": "healthy",
        }

    ###########################################################################

    def summary(self):

        return {
            "supported": [
                "token",
                "deployer",
                "bonding_curve",
                "liquidity",
                "migration",
                "holders",
                "transactions",
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

    creator = data.get("creator")

    if creator:

        addresses.append(creator)

    for holder in data.get("holders", []):

        wallet = holder.get("wallet")

        if wallet:

            addresses.append(wallet)

    return list(set(addresses))