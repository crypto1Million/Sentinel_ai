###############################################################################
# Imports
###############################################################################

from __future__ import annotations

from typing import Any

from .postgres_repository import PostgreSQLRepository

###############################################################################
# WalletRepository
###############################################################################


class WalletRepository(PostgreSQLRepository):
    """
    Wallet Repository.
    """

    ###########################################################################
    # Initialization
    ###########################################################################

    def __init__(
        self,
        engine,
    ) -> None:

        super().__init__(engine)

    ###########################################################################
    # CRUD
    ###########################################################################

    def get_wallet(
        self,
        wallet: str,
    ) -> dict | None:

        query = """
        SELECT *
        FROM wallets
        WHERE wallet=:wallet
        """

        return self.fetch_one(
            query,
            {
                "wallet": wallet,
            },
        )

    ###########################################################################

    def create_wallet(
        self,
        values: dict,
    ):

        return self.insert(
            "wallets",
            values,
        )

    ###########################################################################

    def update_wallet(
        self,
        wallet: str,
        values: dict,
    ):

        return self.update(
            "wallets",
            values,
            {
                "wallet": wallet,
            },
        )

    ###########################################################################

    def delete_wallet(
        self,
        wallet: str,
    ):

        return self.delete(
            "wallets",
            {
                "wallet": wallet,
            },
        )

    ###########################################################################

    def wallet_exists(
        self,
        wallet: str,
    ) -> bool:

        return self.exists(
            "wallets",
            {
                "wallet": wallet,
            },
        )

    ###########################################################################
    # Summary
    ###########################################################################

    def wallet_summary(
        self,
        wallet: str,
    ):

        query = """
        SELECT *
        FROM wallet_summary
        WHERE wallet=:wallet
        """

        return self.fetch_one(
            query,
            {
                "wallet": wallet,
            },
        )

    ###########################################################################

    def wallet_statistics(
        self,
        wallet: str,
    ):

        query = """
        SELECT *
        FROM wallet_statistics
        WHERE wallet=:wallet
        """

        return self.fetch_one(
            query,
            {
                "wallet": wallet,
            },
        )

    ###########################################################################

    def wallet_score(
        self,
        wallet: str,
    ):

        query = """
        SELECT *
        FROM wallet_scores
        WHERE wallet=:wallet
        """

        return self.fetch_one(
            query,
            {
                "wallet": wallet,
            },
        )

    ###########################################################################

    def wallet_traits(
        self,
        wallet: str,
    ):

        query = """
        SELECT *
        FROM wallet_traits
        WHERE wallet=:wallet
        """

        return self.fetch_all(
            query,
            {
                "wallet": wallet,
            },
        )

    ###########################################################################

    def wallet_labels(
        self,
        wallet: str,
    ):

        query = """
        SELECT *
        FROM wallet_labels
        WHERE wallet=:wallet
        """

        return self.fetch_all(
            query,
            {
                "wallet": wallet,
            },
        )

    ###########################################################################

    def wallet_confidence(
        self,
        wallet: str,
    ):

        query = """
        SELECT confidence
        FROM wallet_scores
        WHERE wallet=:wallet
        """

        return self.fetch_one(
            query,
            {
                "wallet": wallet,
            },
        )

    ###########################################################################
    # Relationships
    ###########################################################################

    def wallet_activity(
        self,
        wallet: str,
    ):

        query = """
        SELECT *
        FROM wallet_activity
        WHERE wallet=:wallet
        ORDER BY timestamp DESC
        """

        return self.fetch_all(
            query,
            {
                "wallet": wallet,
            },
        )

    ###########################################################################

    def wallet_tokens(
        self,
        wallet: str,
    ):

        query = """
        SELECT *
        FROM wallet_tokens
        WHERE wallet=:wallet
        """

        return self.fetch_all(
            query,
            {
                "wallet": wallet,
            },
        )

    ###########################################################################

    def wallet_funding(
        self,
        wallet: str,
    ):

        query = """
        SELECT *
        FROM funding_chain
        WHERE wallet=:wallet
        """

        return self.fetch_all(
            query,
            {
                "wallet": wallet,
            },
        )

    ###########################################################################

    def wallet_cluster(
        self,
        wallet: str,
    ):

        query = """
        SELECT *
        FROM clusters
        WHERE wallet=:wallet
        """

        return self.fetch_one(
            query,
            {
                "wallet": wallet,
            },
        )

    ###########################################################################

    def wallet_graph(
        self,
        wallet: str,
    ):

        query = """
        SELECT *
        FROM wallet_graph
        WHERE wallet=:wallet
        """

        return self.fetch_all(
            query,
            {
                "wallet": wallet,
            },
        )

    ###########################################################################

    def wallet_neighbors(
        self,
        wallet: str,
    ):

        query = """
        SELECT *
        FROM wallet_neighbors
        WHERE wallet=:wallet
        """

        return self.fetch_all(
            query,
            {
                "wallet": wallet,
            },
        )

    ###########################################################################
    # Search
    ###########################################################################

    def search_wallet(
        self,
        query: str,
    ):

        sql = """
        SELECT *
        FROM wallets
        WHERE wallet ILIKE :query
        LIMIT 25
        """

        return self.fetch_all(
            sql,
            {
                "query": f"%{query}%",
            },
        )

    ###########################################################################

    def compare_wallets(
        self,
        wallets: list[str],
    ):

        sql = """
        SELECT *
        FROM wallet_scores
        WHERE wallet = ANY(:wallets)
        """

        return self.fetch_all(
            sql,
            {
                "wallets": wallets,
            },
        )

    ###########################################################################
    # Export
    ###########################################################################

    def export_wallet(
        self,
        wallet: str,
    ):

        return self.wallet_summary(wallet)

    ###########################################################################

    def export_wallet_json(
        self,
        wallet: str,
    ):

        return self.wallet_summary(wallet)

    ###########################################################################
    # Health
    ###########################################################################

    def health(
        self,
    ):

        return super().health()

    ###########################################################################

    def diagnostics(
        self,
    ):

        return {
            "repository": "WalletRepository",
            "healthy": self.health(),
        }


###############################################################################
# Runtime
###############################################################################


def summary():

    return {
        "repository": "WalletRepository",
        "table": "wallets",
    }


###############################################################################
# Utilities
###############################################################################


def normalize_wallet(
    wallet: str,
) -> str:

    return wallet.strip()


###############################################################################


def build_wallet(
    row: dict,
) -> dict:

    return row


###############################################################################


def cache_wallet(
    wallet: str,
) -> str:

    return f"wallet:{wallet}"


###############################################################################


def wallet_metadata(
    wallet: str,
) -> dict:

    return {
        "wallet": wallet,
    }