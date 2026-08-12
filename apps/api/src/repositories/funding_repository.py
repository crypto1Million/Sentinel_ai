###############################################################################
# Imports
###############################################################################

from __future__ import annotations

from typing import Any

from .postgres_repository import PostgreSQLRepository

###############################################################################
# FundingRepository
###############################################################################


class FundingRepository(PostgreSQLRepository):
    """
    Funding Repository.
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

    def get_funding(
        self,
        funding_id: str,
    ) -> dict | None:

        query = """
        SELECT *
        FROM funding
        WHERE funding_id=:funding_id
        """

        return self.fetch_one(
            query,
            {
                "funding_id": funding_id,
            },
        )

    ###########################################################################

    def create_funding(
        self,
        values: dict,
    ):

        return self.insert(
            "funding",
            values,
        )

    ###########################################################################

    def update_funding(
        self,
        funding_id: str,
        values: dict,
    ):

        return self.update(
            "funding",
            values,
            {
                "funding_id": funding_id,
            },
        )

    ###########################################################################

    def delete_funding(
        self,
        funding_id: str,
    ):

        return self.delete(
            "funding",
            {
                "funding_id": funding_id,
            },
        )

    ###########################################################################

    def funding_exists(
        self,
        funding_id: str,
    ) -> bool:

        return self.exists(
            "funding",
            {
                "funding_id": funding_id,
            },
        )

    ###########################################################################
    # Funding Chain
    ###########################################################################

    def funding_chain(
        self,
        wallet: str,
    ):

        query = """
        SELECT *
        FROM funding_chain
        WHERE wallet=:wallet
        ORDER BY depth ASC
        """

        return self.fetch_all(
            query,
            {
                "wallet": wallet,
            },
        )

    ###########################################################################

    def funding_nodes(
        self,
        wallet: str,
    ):

        query = """
        SELECT *
        FROM funding_nodes
        WHERE wallet=:wallet
        """

        return self.fetch_all(
            query,
            {
                "wallet": wallet,
            },
        )

    ###########################################################################

    def funding_edges(
        self,
        wallet: str,
    ):

        query = """
        SELECT *
        FROM funding_edges
        WHERE wallet=:wallet
        """

        return self.fetch_all(
            query,
            {
                "wallet": wallet,
            },
        )

    ###########################################################################

    def funding_statistics(
        self,
        wallet: str,
    ):

        query = """
        SELECT *
        FROM funding_statistics
        WHERE wallet=:wallet
        """

        return self.fetch_one(
            query,
            {
                "wallet": wallet,
            },
        )

    ###########################################################################

    def funding_score(
        self,
        wallet: str,
    ):

        query = """
        SELECT *
        FROM funding_scores
        WHERE wallet=:wallet
        """

        return self.fetch_one(
            query,
            {
                "wallet": wallet,
            },
        )

    ###########################################################################

    def funding_graph(
        self,
        wallet: str,
    ):

        query = """
        SELECT *
        FROM funding_graph
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

    def search_funding(
        self,
        query: str,
    ):

        sql = """
        SELECT *
        FROM funding
        WHERE source_wallet ILIKE :query
           OR destination_wallet ILIKE :query
           OR signature ILIKE :query
        LIMIT 50
        """

        return self.fetch_all(
            sql,
            {
                "query": f"%{query}%",
            },
        )

    ###########################################################################
    # Export
    ###########################################################################

    def export_funding(
        self,
        wallet: str,
    ):

        return {
            "wallet": wallet,
            "chain": self.funding_chain(wallet),
            "statistics": self.funding_statistics(wallet),
            "score": self.funding_score(wallet),
        }

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
            "repository": "FundingRepository",
            "healthy": self.health(),
        }


###############################################################################
# Runtime
###############################################################################


def summary():

    return {
        "repository": "FundingRepository",
        "table": "funding",
    }


###############################################################################
# Utilities
###############################################################################


def normalize_funding(
    funding_id: str,
) -> str:

    return funding_id.strip()


###############################################################################


def build_funding(
    row: dict,
) -> dict:

    return row


###############################################################################


def cache_funding(
    funding_id: str,
) -> str:

    return f"funding:{funding_id}"


###############################################################################


def funding_metadata(
    funding_id: str,
) -> dict:

    return {
        "funding_id": funding_id,
    }