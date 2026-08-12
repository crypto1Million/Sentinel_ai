###############################################################################
# Imports
###############################################################################

from __future__ import annotations

from .postgres_repository import PostgreSQLRepository

###############################################################################
# DeployerRepository
###############################################################################


class DeployerRepository(PostgreSQLRepository):
    """
    Repository for deployer intelligence.
    """

    ###########################################################################
    # Initialization
    ###########################################################################

    def __init__(self, engine):

        super().__init__(engine)

    ###########################################################################
    # CRUD
    ###########################################################################

    def get_deployer(self, deployer: str):

        query = """
        SELECT *
        FROM deployers
        WHERE deployer=:deployer
        """

        return self.fetch_one(query, {"deployer": deployer})

    ###########################################################################

    def create_deployer(self, values: dict):

        return self.insert("deployers", values)

    ###########################################################################

    def update_deployer(self, deployer: str, values: dict):

        return self.update(
            "deployers",
            values,
            {"deployer": deployer},
        )

    ###########################################################################

    def delete_deployer(self, deployer: str):

        return self.delete(
            "deployers",
            {"deployer": deployer},
        )

    ###########################################################################

    def deployer_exists(self, deployer: str):

        return self.exists(
            "deployers",
            {"deployer": deployer},
        )

    ###########################################################################
    # Summary
    ###########################################################################

    def deployer_summary(self, deployer: str):

        query = """
        SELECT *
        FROM deployer_summary
        WHERE deployer=:deployer
        """

        return self.fetch_one(query, {"deployer": deployer})

    ###########################################################################

    def deployer_statistics(self, deployer: str):

        query = """
        SELECT *
        FROM deployer_statistics
        WHERE deployer=:deployer
        """

        return self.fetch_one(query, {"deployer": deployer})

    ###########################################################################

    def deployer_tokens(self, deployer: str):

        query = """
        SELECT *
        FROM deployer_tokens
        WHERE deployer=:deployer
        """

        return self.fetch_all(query, {"deployer": deployer})

    ###########################################################################

    def deployer_wallets(self, deployer: str):

        query = """
        SELECT *
        FROM deployer_wallets
        WHERE deployer=:deployer
        """

        return self.fetch_all(query, {"deployer": deployer})

    ###########################################################################

    def deployer_funding(self, deployer: str):

        query = """
        SELECT *
        FROM funding_chain
        WHERE deployer=:deployer
        """

        return self.fetch_all(query, {"deployer": deployer})

    ###########################################################################

    def deployer_history(self, deployer: str):

        query = """
        SELECT *
        FROM deployer_history
        WHERE deployer=:deployer
        ORDER BY timestamp DESC
        """

        return self.fetch_all(query, {"deployer": deployer})

    ###########################################################################

    def deployer_graph(self, deployer: str):

        query = """
        SELECT *
        FROM deployer_graph
        WHERE deployer=:deployer
        """

        return self.fetch_all(query, {"deployer": deployer})

    ###########################################################################

    def deployer_score(self, deployer: str):

        query = """
        SELECT *
        FROM deployer_scores
        WHERE deployer=:deployer
        """

        return self.fetch_one(query, {"deployer": deployer})

    ###########################################################################
    # Comparison
    ###########################################################################

    def compare_deployers(self, deployers: list[str]):

        query = """
        SELECT *
        FROM deployer_scores
        WHERE deployer = ANY(:deployers)
        """

        return self.fetch_all(
            query,
            {"deployers": deployers},
        )

    ###########################################################################
    # Export
    ###########################################################################

    def export_deployer(self, deployer: str):

        return {
            "summary": self.deployer_summary(deployer),
            "statistics": self.deployer_statistics(deployer),
            "tokens": self.deployer_tokens(deployer),
            "wallets": self.deployer_wallets(deployer),
            "funding": self.deployer_funding(deployer),
            "history": self.deployer_history(deployer),
            "graph": self.deployer_graph(deployer),
            "score": self.deployer_score(deployer),
        }

    ###########################################################################
    # Health
    ###########################################################################

    def health(self):

        return super().health()

    ###########################################################################

    def diagnostics(self):

        return {
            "repository": "DeployerRepository",
            "healthy": self.health(),
        }


###############################################################################
# Runtime
###############################################################################


def summary():

    return {
        "repository": "DeployerRepository",
        "table": "deployers",
    }


###############################################################################
# Utilities
###############################################################################


def normalize_deployer(deployer: str):

    return deployer.strip()


###############################################################################


def build_deployer(row: dict):

    return row


###############################################################################


def cache_deployer(deployer: str):

    return f"deployer:{deployer}"


###############################################################################


def deployer_metadata(deployer: str):

    return {
        "deployer": deployer,
    }