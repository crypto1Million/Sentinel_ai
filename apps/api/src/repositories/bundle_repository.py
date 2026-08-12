###############################################################################
# Imports
###############################################################################

from __future__ import annotations

from typing import Any

from .postgres_repository import PostgreSQLRepository

###############################################################################
# BundleRepository
###############################################################################


class BundleRepository(PostgreSQLRepository):
    """
    Bundle Repository.
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

    def get_bundle(
        self,
        bundle_id: str,
    ) -> dict | None:

        query = """
        SELECT *
        FROM bundles
        WHERE bundle_id=:bundle_id
        """

        return self.fetch_one(
            query,
            {
                "bundle_id": bundle_id,
            },
        )

    ###########################################################################

    def create_bundle(
        self,
        values: dict,
    ):

        return self.insert(
            "bundles",
            values,
        )

    ###########################################################################

    def update_bundle(
        self,
        bundle_id: str,
        values: dict,
    ):

        return self.update(
            "bundles",
            values,
            {
                "bundle_id": bundle_id,
            },
        )

    ###########################################################################

    def delete_bundle(
        self,
        bundle_id: str,
    ):

        return self.delete(
            "bundles",
            {
                "bundle_id": bundle_id,
            },
        )

    ###########################################################################

    def bundle_exists(
        self,
        bundle_id: str,
    ) -> bool:

        return self.exists(
            "bundles",
            {
                "bundle_id": bundle_id,
            },
        )

    ###########################################################################
    # Bundle Summary
    ###########################################################################

    def bundle_summary(
        self,
        bundle_id: str,
    ):

        query = """
        SELECT *
        FROM bundle_summary
        WHERE bundle_id=:bundle_id
        """

        return self.fetch_one(
            query,
            {
                "bundle_id": bundle_id,
            },
        )

    ###########################################################################

    def bundle_wallets(
        self,
        bundle_id: str,
    ):

        query = """
        SELECT *
        FROM bundle_wallets
        WHERE bundle_id=:bundle_id
        """

        return self.fetch_all(
            query,
            {
                "bundle_id": bundle_id,
            },
        )

    ###########################################################################

    def bundle_tokens(
        self,
        bundle_id: str,
    ):

        query = """
        SELECT *
        FROM bundle_tokens
        WHERE bundle_id=:bundle_id
        """

        return self.fetch_all(
            query,
            {
                "bundle_id": bundle_id,
            },
        )

    ###########################################################################

    def bundle_statistics(
        self,
        bundle_id: str,
    ):

        query = """
        SELECT *
        FROM bundle_statistics
        WHERE bundle_id=:bundle_id
        """

        return self.fetch_one(
            query,
            {
                "bundle_id": bundle_id,
            },
        )

    ###########################################################################

    def bundle_score(
        self,
        bundle_id: str,
    ):

        query = """
        SELECT *
        FROM bundle_scores
        WHERE bundle_id=:bundle_id
        """

        return self.fetch_one(
            query,
            {
                "bundle_id": bundle_id,
            },
        )

    ###########################################################################

    def bundle_graph(
        self,
        bundle_id: str,
    ):

        query = """
        SELECT *
        FROM bundle_graph
        WHERE bundle_id=:bundle_id
        """

        return self.fetch_all(
            query,
            {
                "bundle_id": bundle_id,
            },
        )

    ###########################################################################
    # Detection
    ###########################################################################

    def detect_bundle(
        self,
        wallet: str,
    ):

        query = """
        SELECT *
        FROM bundles
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

    def search_bundle(
        self,
        query: str,
    ):

        sql = """
        SELECT *
        FROM bundles
        WHERE bundle_id ILIKE :query
           OR wallet ILIKE :query
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

    def export_bundle(
        self,
        bundle_id: str,
    ):

        return {
            "summary": self.bundle_summary(bundle_id),
            "wallets": self.bundle_wallets(bundle_id),
            "tokens": self.bundle_tokens(bundle_id),
            "statistics": self.bundle_statistics(bundle_id),
            "score": self.bundle_score(bundle_id),
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
            "repository": "BundleRepository",
            "healthy": self.health(),
        }


###############################################################################
# Runtime
###############################################################################


def summary():

    return {
        "repository": "BundleRepository",
        "table": "bundles",
    }


###############################################################################
# Utilities
###############################################################################


def normalize_bundle(
    bundle_id: str,
) -> str:

    return bundle_id.strip()


###############################################################################


def build_bundle(
    row: dict,
) -> dict:

    return row


###############################################################################


def cache_bundle(
    bundle_id: str,
) -> str:

    return f"bundle:{bundle_id}"


###############################################################################


def bundle_metadata(
    bundle_id: str,
) -> dict:

    return {
        "bundle_id": bundle_id,
    }