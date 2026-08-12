###############################################################################
# Imports
###############################################################################

from __future__ import annotations

from .postgres_repository import PostgreSQLRepository

###############################################################################
# WalletDNARepository
###############################################################################


class WalletDNARepository(PostgreSQLRepository):
    """
    Wallet DNA Repository.
    """

    ###########################################################################
    # Initialization
    ###########################################################################

    def __init__(self, engine):

        super().__init__(engine)

    ###########################################################################
    # CRUD
    ###########################################################################

    def get_wallet_dna(
        self,
        wallet: str,
    ):

        return self.fetch_one(
            """
            SELECT *
            FROM wallet_dna
            WHERE wallet=:wallet
            """,
            {"wallet": wallet},
        )

    ###########################################################################

    def create_wallet_dna(
        self,
        values: dict,
    ):

        return self.insert(
            "wallet_dna",
            values,
        )

    ###########################################################################

    def update_wallet_dna(
        self,
        wallet: str,
        values: dict,
    ):

        return self.update(
            "wallet_dna",
            values,
            {"wallet": wallet},
        )

    ###########################################################################

    def delete_wallet_dna(
        self,
        wallet: str,
    ):

        return self.delete(
            "wallet_dna",
            {"wallet": wallet},
        )

    ###########################################################################

    def dna_exists(
        self,
        wallet: str,
    ):

        return self.exists(
            "wallet_dna",
            {"wallet": wallet},
        )

    ###########################################################################
    # Scores
    ###########################################################################

    def wallet_score(
        self,
        wallet: str,
    ):

        return self.fetch_one(
            """
            SELECT wallet_score
            FROM wallet_dna
            WHERE wallet=:wallet
            """,
            {"wallet": wallet},
        )

    ###########################################################################

    def conviction_score(
        self,
        wallet: str,
    ):

        return self.fetch_one(
            """
            SELECT conviction_score
            FROM wallet_dna
            WHERE wallet=:wallet
            """,
            {"wallet": wallet},
        )

    ###########################################################################

    def narrative_score(
        self,
        wallet: str,
    ):

        return self.fetch_one(
            """
            SELECT narrative_score
            FROM wallet_dna
            WHERE wallet=:wallet
            """,
            {"wallet": wallet},
        )

    ###########################################################################

    def risk_score(
        self,
        wallet: str,
    ):

        return self.fetch_one(
            """
            SELECT risk_score
            FROM wallet_dna
            WHERE wallet=:wallet
            """,
            {"wallet": wallet},
        )

    ###########################################################################

    def confidence(
        self,
        wallet: str,
    ):

        return self.fetch_one(
            """
            SELECT confidence
            FROM wallet_dna
            WHERE wallet=:wallet
            """,
            {"wallet": wallet},
        )

    ###########################################################################

    def ai_explanation(
        self,
        wallet: str,
    ):

        return self.fetch_one(
            """
            SELECT explanation
            FROM wallet_dna
            WHERE wallet=:wallet
            """,
            {"wallet": wallet},
        )

    ###########################################################################
    # Traits
    ###########################################################################

    def wallet_traits(
        self,
        wallet: str,
    ):

        return self.fetch_all(
            """
            SELECT *
            FROM wallet_traits
            WHERE wallet=:wallet
            """,
            {"wallet": wallet},
        )

    ###########################################################################

    def wallet_labels(
        self,
        wallet: str,
    ):

        return self.fetch_all(
            """
            SELECT *
            FROM wallet_labels
            WHERE wallet=:wallet
            """,
            {"wallet": wallet},
        )

    ###########################################################################

    def wallet_behavior(
        self,
        wallet: str,
    ):

        return self.fetch_all(
            """
            SELECT *
            FROM wallet_behavior
            WHERE wallet=:wallet
            """,
            {"wallet": wallet},
        )

    ###########################################################################

    def wallet_personality(
        self,
        wallet: str,
    ):

        return self.fetch_one(
            """
            SELECT *
            FROM wallet_personality
            WHERE wallet=:wallet
            """,
            {"wallet": wallet},
        )

    ###########################################################################
    # Search
    ###########################################################################

    def search_wallet_dna(
        self,
        query: str,
    ):

        return self.fetch_all(
            """
            SELECT *
            FROM wallet_dna
            WHERE wallet ILIKE :query
            LIMIT 50
            """,
            {
                "query": f"%{query}%"
            },
        )

    ###########################################################################

    def compare_wallet_dna(
        self,
        wallets: list[str],
    ):

        return self.fetch_all(
            """
            SELECT *
            FROM wallet_dna
            WHERE wallet = ANY(:wallets)
            """,
            {
                "wallets": wallets
            },
        )

    ###########################################################################
    # Export
    ###########################################################################

    def export_wallet_dna(
        self,
        wallet: str,
    ):

        return self.get_wallet_dna(
            wallet,
        )

    ###########################################################################

    def export_json(
        self,
        wallet: str,
    ):

        return self.export_wallet_dna(
            wallet,
        )

    ###########################################################################
    # Health
    ###########################################################################

    def health(self):

        return super().health()

    ###########################################################################

    def diagnostics(self):

        return {
            "repository": "WalletDNARepository",
            "healthy": self.health(),
        }


###############################################################################
# Runtime
###############################################################################


def summary():

    return {
        "repository": "WalletDNARepository",
    }


###############################################################################
# Utilities
###############################################################################


def normalize_wallet(
    wallet: str,
):

    return wallet.strip()


###############################################################################


def cache_wallet_dna(
    wallet: str,
):

    return f"wallet_dna:{wallet}"


###############################################################################


def metadata(
    wallet: str,
):

    return {
        "wallet": wallet,
    }