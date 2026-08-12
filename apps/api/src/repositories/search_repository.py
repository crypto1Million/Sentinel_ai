###############################################################################
# Imports
###############################################################################

from __future__ import annotations

from .postgres_repository import PostgreSQLRepository

###############################################################################
# SearchRepository
###############################################################################


class SearchRepository(PostgreSQLRepository):
    """
    Global Search Repository.
    """

    ###########################################################################
    # Initialization
    ###########################################################################

    def __init__(self, engine):

        super().__init__(engine)

    ###########################################################################
    # Search
    ###########################################################################

    def global_search(
        self,
        query: str,
    ):

        return self.raw_query(
            """
            SELECT *
            FROM global_search(:query)
            """,
            {"query": query},
        )

    ###########################################################################

    def search_wallet(
        self,
        wallet: str,
    ):

        return self.fetch_all(
            """
            SELECT *
            FROM wallets
            WHERE wallet ILIKE :wallet
            """,
            {
                "wallet": f"%{wallet}%"
            },
        )

    ###########################################################################

    def search_token(
        self,
        token: str,
    ):

        return self.fetch_all(
            """
            SELECT *
            FROM tokens
            WHERE symbol ILIKE :token
               OR mint ILIKE :token
            """,
            {
                "token": f"%{token}%"
            },
        )

    ###########################################################################

    def search_bundle(
        self,
        bundle: str,
    ):

        return self.fetch_all(
            """
            SELECT *
            FROM bundles
            WHERE bundle_id ILIKE :bundle
            """,
            {
                "bundle": f"%{bundle}%"
            },
        )

    ###########################################################################

    def search_deployer(
        self,
        deployer: str,
    ):

        return self.fetch_all(
            """
            SELECT *
            FROM deployers
            WHERE deployer ILIKE :deployer
            """,
            {
                "deployer": f"%{deployer}%"
            },
        )

    ###########################################################################

    def search_cluster(
        self,
        cluster: str,
    ):

        return self.fetch_all(
            """
            SELECT *
            FROM clusters
            WHERE cluster_id ILIKE :cluster
            """,
            {
                "cluster": f"%{cluster}%"
            },
        )

    ###########################################################################

    def search_graph(
        self,
        graph: str,
    ):

        return self.raw_query(
            """
            SELECT *
            FROM graph_search(:graph)
            """,
            {"graph": graph},
        )

    ###########################################################################

    def autocomplete(
        self,
        prefix: str,
    ):

        return self.fetch_all(
            """
            SELECT suggestion
            FROM autocomplete
            WHERE suggestion ILIKE :prefix
            LIMIT 20
            """,
            {
                "prefix": f"{prefix}%"
            },
        )

    ###########################################################################

    def recent_searches(self):

        return self.fetch_all(
            """
            SELECT *
            FROM search_history
            ORDER BY searched_at DESC
            LIMIT 20
            """
        )

    ###########################################################################
    # Advanced
    ###########################################################################

    def advanced_search(
        self,
        filters: dict,
    ):

        return self.raw_query(
            """
            SELECT *
            FROM advanced_search(:filters)
            """,
            {"filters": filters},
        )

    ###########################################################################

    def save_search(
        self,
        values: dict,
    ):

        return self.insert(
            "saved_searches",
            values,
        )

    ###########################################################################

    def search_history(self):

        return self.fetch_all(
            """
            SELECT *
            FROM search_history
            ORDER BY searched_at DESC
            """
        )

    ###########################################################################
    # Health
    ###########################################################################

    def health(self):

        return super().health()

    ###########################################################################

    def diagnostics(self):

        return {
            "repository": "SearchRepository",
            "healthy": self.health(),
        }


###############################################################################
# Runtime
###############################################################################


def summary():

    return {
        "repository": "SearchRepository",
    }


###############################################################################
# Utilities
###############################################################################


def normalize_query(
    query: str,
):

    return query.strip().lower()


###############################################################################


def cache_search(
    query: str,
):

    return f"search:{query}"


###############################################################################


def metadata():

    return {
        "module": "SearchRepository",
    }