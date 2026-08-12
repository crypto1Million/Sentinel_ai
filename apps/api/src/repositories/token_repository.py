###############################################################################
# Imports
###############################################################################

from __future__ import annotations

from typing import Any

from .postgres_repository import PostgreSQLRepository

###############################################################################
# TokenRepository
###############################################################################


class TokenRepository(PostgreSQLRepository):
    """
    Token Repository.
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

    def get_token(
        self,
        mint: str,
    ) -> dict | None:

        query = """
        SELECT *
        FROM tokens
        WHERE mint=:mint
        """

        return self.fetch_one(
            query,
            {
                "mint": mint,
            },
        )

    ###########################################################################

    def create_token(
        self,
        values: dict,
    ):

        return self.insert(
            "tokens",
            values,
        )

    ###########################################################################

    def update_token(
        self,
        mint: str,
        values: dict,
    ):

        return self.update(
            "tokens",
            values,
            {
                "mint": mint,
            },
        )

    ###########################################################################

    def delete_token(
        self,
        mint: str,
    ):

        return self.delete(
            "tokens",
            {
                "mint": mint,
            },
        )

    ###########################################################################

    def token_exists(
        self,
        mint: str,
    ) -> bool:

        return self.exists(
            "tokens",
            {
                "mint": mint,
            },
        )

    ###########################################################################
    # Summary
    ###########################################################################

    def token_summary(
        self,
        mint: str,
    ):

        query = """
        SELECT *
        FROM token_summary
        WHERE mint=:mint
        """

        return self.fetch_one(
            query,
            {
                "mint": mint,
            },
        )

    ###########################################################################

    def token_statistics(
        self,
        mint: str,
    ):

        query = """
        SELECT *
        FROM token_statistics
        WHERE mint=:mint
        """

        return self.fetch_one(
            query,
            {
                "mint": mint,
            },
        )

    ###########################################################################

    def token_score(
        self,
        mint: str,
    ):

        query = """
        SELECT *
        FROM token_scores
        WHERE mint=:mint
        """

        return self.fetch_one(
            query,
            {
                "mint": mint,
            },
        )

    ###########################################################################
    # Relationships
    ###########################################################################

    def token_holders(
        self,
        mint: str,
    ):

        query = """
        SELECT *
        FROM token_holders
        WHERE mint=:mint
        """

        return self.fetch_all(
            query,
            {
                "mint": mint,
            },
        )

    ###########################################################################

    def token_transactions(
        self,
        mint: str,
    ):

        query = """
        SELECT *
        FROM token_transactions
        WHERE mint=:mint
        ORDER BY timestamp DESC
        """

        return self.fetch_all(
            query,
            {
                "mint": mint,
            },
        )

    ###########################################################################

    def token_funding(
        self,
        mint: str,
    ):

        query = """
        SELECT *
        FROM funding_chain
        WHERE mint=:mint
        """

        return self.fetch_all(
            query,
            {
                "mint": mint,
            },
        )

    ###########################################################################

    def token_bundle(
        self,
        mint: str,
    ):

        query = """
        SELECT *
        FROM bundles
        WHERE mint=:mint
        """

        return self.fetch_all(
            query,
            {
                "mint": mint,
            },
        )

    ###########################################################################

    def token_graph(
        self,
        mint: str,
    ):

        query = """
        SELECT *
        FROM token_graph
        WHERE mint=:mint
        """

        return self.fetch_all(
            query,
            {
                "mint": mint,
            },
        )

    ###########################################################################
    # Search
    ###########################################################################

    def search_token(
        self,
        query: str,
    ):

        sql = """
        SELECT *
        FROM tokens
        WHERE symbol ILIKE :query
           OR name ILIKE :query
           OR mint ILIKE :query
        LIMIT 25
        """

        return self.fetch_all(
            sql,
            {
                "query": f"%{query}%",
            },
        )

    ###########################################################################

    def compare_tokens(
        self,
        mints: list[str],
    ):

        sql = """
        SELECT *
        FROM token_scores
        WHERE mint = ANY(:mints)
        """

        return self.fetch_all(
            sql,
            {
                "mints": mints,
            },
        )

    ###########################################################################
    # Export
    ###########################################################################

    def export_token(
        self,
        mint: str,
    ):

        return self.token_summary(mint)

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
            "repository": "TokenRepository",
            "healthy": self.health(),
        }


###############################################################################
# Runtime
###############################################################################


def summary():

    return {
        "repository": "TokenRepository",
        "table": "tokens",
    }


###############################################################################
# Utilities
###############################################################################


def normalize_token(
    mint: str,
) -> str:

    return mint.strip()


###############################################################################


def build_token(
    row: dict,
) -> dict:

    return row


###############################################################################


def cache_token(
    mint: str,
) -> str:

    return f"token:{mint}"


###############################################################################


def token_metadata(
    mint: str,
) -> dict:

    return {
        "mint": mint,
    }