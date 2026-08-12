"""
Helius Parser
=============

Parsers for Helius Enhanced Transactions, Wallets, Tokens and Metadata.
"""

###############################################################################
# Imports
###############################################################################

from __future__ import annotations

from typing import Any, Dict, List

###############################################################################
# Transaction Parser
###############################################################################


class HeliusParser:
    """
    Parses Helius API responses into normalized Sentinel objects.
    """

    ###########################################################################

    def parse_transaction(
        self,
        data: Dict,
    ) -> Dict:

        return normalize(
            {
                "signature": data.get("signature"),
                "slot": data.get("slot"),
                "timestamp": data.get("timestamp"),
                "fee": data.get("fee"),
                "accounts": extract_accounts(data),
            }
        )

    ###########################################################################

    def parse_wallet(
        self,
        data: Dict,
    ) -> Dict:

        return normalize(
            {
                "wallet": data.get("account"),
                "balance": data.get("nativeBalance"),
                "owner": data.get("owner"),
            }
        )

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

    def parse_swap(
        self,
        data: Dict,
    ) -> Dict:

        return normalize(
            {
                "source": data.get("sourceMint"),
                "destination": data.get("destinationMint"),
                "amount_in": data.get("amountIn"),
                "amount_out": data.get("amountOut"),
            }
        )

    ###########################################################################

    def parse_transfer(
        self,
        data: Dict,
    ) -> Dict:

        return normalize(
            {
                "from": data.get("fromUserAccount"),
                "to": data.get("toUserAccount"),
                "amount": data.get("tokenAmount"),
            }
        )

    ###########################################################################

    def parse_instruction(
        self,
        instruction: Dict,
    ) -> Dict:

        return normalize(
            {
                "program": instruction.get("programId"),
                "type": instruction.get("type"),
                "data": instruction.get("data"),
            }
        )

    ###########################################################################

    def parse_logs(
        self,
        data: Dict,
    ) -> List:

        return data.get("logMessages", [])

    ###########################################################################

    def parse_metadata(
        self,
        data: Dict,
    ) -> Dict:

        return normalize(
            {
                "name": data.get("name"),
                "symbol": data.get("symbol"),
                "uri": data.get("uri"),
                "collection": data.get("collection"),
            }
        )

    ###########################################################################
    # Runtime
    ###########################################################################

    def diagnostics(self):

        return {
            "parser": "HeliusParser",
            "status": "healthy",
        }

    ###########################################################################

    def summary(self):

        return {
            "supported": [
                "transaction",
                "wallet",
                "token",
                "swap",
                "transfer",
                "instruction",
                "logs",
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


def extract_accounts(
    transaction: Dict,
) -> List[str]:

    accounts = []

    for acc in transaction.get("accountData", []):

        account = acc.get("account")

        if account:

            accounts.append(account)

    return accounts