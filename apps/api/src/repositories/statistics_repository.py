###############################################################################
# Imports
###############################################################################

from __future__ import annotations

from .postgres_repository import PostgreSQLRepository

###############################################################################
# StatisticsRepository
###############################################################################


class StatisticsRepository(PostgreSQLRepository):
    """
    Statistics Repository.
    """

    ###########################################################################
    # Initialization
    ###########################################################################

    def __init__(self, engine):

        super().__init__(engine)

    ###########################################################################
    # Global
    ###########################################################################

    def global_statistics(self):

        return self.fetch_one(
            """
            SELECT *
            FROM global_statistics
            LIMIT 1
            """
        )

    ###########################################################################

    def runtime_statistics(self):

        return self.fetch_one(
            """
            SELECT *
            FROM runtime_statistics
            LIMIT 1
            """
        )

    ###########################################################################

    def dashboard_metrics(self):

        return self.fetch_one(
            """
            SELECT *
            FROM dashboard_metrics
            LIMIT 1
            """
        )

    ###########################################################################

    def wallet_statistics(self):

        return self.fetch_one(
            """
            SELECT *
            FROM wallet_statistics
            LIMIT 1
            """
        )

    ###########################################################################

    def token_statistics(self):

        return self.fetch_one(
            """
            SELECT *
            FROM token_statistics
            LIMIT 1
            """
        )

    ###########################################################################

    def funding_statistics(self):

        return self.fetch_one(
            """
            SELECT *
            FROM funding_statistics
            LIMIT 1
            """
        )

    ###########################################################################

    def bundle_statistics(self):

        return self.fetch_one(
            """
            SELECT *
            FROM bundle_statistics
            LIMIT 1
            """
        )

    ###########################################################################

    def deployer_statistics(self):

        return self.fetch_one(
            """
            SELECT *
            FROM deployer_statistics
            LIMIT 1
            """
        )

    ###########################################################################

    def cluster_statistics(self):

        return self.fetch_one(
            """
            SELECT *
            FROM cluster_statistics
            LIMIT 1
            """
        )

    ###########################################################################

    def graph_statistics(self):

        return self.fetch_one(
            """
            SELECT *
            FROM graph_statistics
            LIMIT 1
            """
        )

    ###########################################################################
    # Refresh
    ###########################################################################

    def refresh_statistics(self):

        return self.execute(
            """
            REFRESH MATERIALIZED VIEW CONCURRENTLY global_statistics
            """
        )

    ###########################################################################

    def rebuild_statistics(self):

        return self.execute(
            """
            CALL rebuild_statistics()
            """
        )

    ###########################################################################

    def cache_statistics(self):

        return {
            "cached": True,
        }

    ###########################################################################
    # Export
    ###########################################################################

    def export_statistics(self):

        return {
            "global": self.global_statistics(),
            "runtime": self.runtime_statistics(),
            "dashboard": self.dashboard_metrics(),
            "wallet": self.wallet_statistics(),
            "token": self.token_statistics(),
            "funding": self.funding_statistics(),
            "bundle": self.bundle_statistics(),
            "deployer": self.deployer_statistics(),
            "cluster": self.cluster_statistics(),
            "graph": self.graph_statistics(),
        }

    ###########################################################################

    def export_dashboard(self):

        return self.dashboard_metrics()

    ###########################################################################
    # Health
    ###########################################################################

    def health(self):

        return super().health()

    ###########################################################################

    def diagnostics(self):

        return {
            "repository": "StatisticsRepository",
            "healthy": self.health(),
        }


###############################################################################
# Runtime
###############################################################################


def summary():

    return {
        "repository": "StatisticsRepository",
    }


###############################################################################
# Utilities
###############################################################################


def statistics_metadata():

    return {
        "source": "statistics_repository",
    }


###############################################################################


def cache_key():

    return "statistics:global"