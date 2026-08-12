"""
Mock Helius Integration
=======================

Fake Helius/Solana data provider used by Sentinel AI tests.
"""

from __future__ import annotations

from typing import Any, Dict, List


class MockHelius:

    def __init__(self):

        self.wallets: Dict[str, Dict[str, Any]] = {}
        self.transactions: Dict[str, List[Dict[str, Any]]] = {}
        self.token_holders: Dict[str, List[Dict[str, Any]]] = {}

    # ------------------------------------------------------------------
    # Wallet
    # ------------------------------------------------------------------

    def get_wallet(self, wallet: str):

        return self.wallets.get(
            wallet,
            {
                "address": wallet,
                "balance": 0.0,
                "tokens": [],
            },
        )

    def get_balance(self, wallet: str):

        return self.get_wallet(wallet)["balance"]

    def get_token_accounts(self, wallet: str):

        return self.get_wallet(wallet)["tokens"]

    # ------------------------------------------------------------------
    # Transactions
    # ------------------------------------------------------------------

    def get_transactions(self, wallet: str):

        return self.transactions.get(
            wallet,
            [],
        )

    # ------------------------------------------------------------------
    # Token Holders
    # ------------------------------------------------------------------

    def get_token_holders(self, mint: str):

        return self.token_holders.get(
            mint,
            [],
        )

    # ------------------------------------------------------------------
    # Test Data
    # ------------------------------------------------------------------

    def add_wallet(
        self,
        wallet: str,
        balance: float = 0.0,
        tokens: List[str] | None = None,
    ):

        self.wallets[wallet] = {
            "address": wallet,
            "balance": balance,
            "tokens": tokens or [],
        }

    def add_transaction(
        self,
        wallet: str,
        transaction: Dict[str, Any],
    ):

        self.transactions.setdefault(
            wallet,
            [],
        ).append(transaction)

    def add_token_holders(
        self,
        mint: str,
        holders: List[Dict[str, Any]],
    ):

        self.token_holders[mint] = holders

    # ------------------------------------------------------------------
    # Runtime
    # ------------------------------------------------------------------

    def diagnostics(self):

        return {
            "connected": True,
            "wallets": len(self.wallets),
            "transaction_wallets": len(
                self.transactions
            ),
            "tokens": len(
                self.token_holders
            ),
        }

    def summary(self):

        return {
            "service": "mock-helius",
            "wallets": len(self.wallets),
            "tokens": len(
                self.token_holders
            ),
        }


# ----------------------------------------------------------------------
# Factory
# ----------------------------------------------------------------------

def mock_helius() -> MockHelius:

    helius = MockHelius()

    helius.add_wallet(
        wallet="Wallet001",
        balance=25.4,
        tokens=["TOKEN001"],
    )

    helius.add_wallet(
        wallet="Wallet002",
        balance=12.7,
        tokens=["TOKEN001"],
    )

    helius.add_transaction(
        "Wallet001",
        {
            "signature": "TX001",
            "from": "Wallet001",
            "to": "Wallet002",
            "amount": 1.5,
        },
    )

    helius.add_token_holders(
        "TOKEN001",
        [
            {
                "wallet": "Wallet001",
                "percentage": 12.5,
            },
            {
                "wallet": "Wallet002",
                "percentage": 7.4,
            },
        ],
    )

    return helius