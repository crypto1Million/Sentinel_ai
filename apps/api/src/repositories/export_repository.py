###############################################################################
# Imports
###############################################################################

from __future__ import annotations

import hashlib
import json
import gzip
from datetime import datetime

from .wallet_repository import WalletRepository
from .token_repository import TokenRepository
from .graph_repository import GraphRepository
from .statistics_repository import StatisticsRepository

###############################################################################
# ExportRepository
###############################################################################


class ExportRepository:
    """
    Sentinel Export Repository.
    """

    ###########################################################################
    # Initialization
    ###########################################################################

    def __init__(
        self,
        wallet_repository: WalletRepository,
        token_repository: TokenRepository,
        graph_repository: GraphRepository,
        statistics_repository: StatisticsRepository,
    ):

        self.wallets = wallet_repository
        self.tokens = token_repository
        self.graphs = graph_repository
        self.statistics = statistics_repository

    ###########################################################################
    # Wallet Export
    ###########################################################################

    def export_wallet_json(
        self,
        wallet: str,
    ):

        return self.wallets.export_wallet(wallet)

    ###########################################################################

    def export_wallet_csv(
        self,
        wallet: str,
    ):

        return self.wallets.export_wallet(wallet)

    ###########################################################################

    def export_wallet_pdf(
        self,
        wallet: str,
    ):

        return self.wallets.export_wallet(wallet)

    ###########################################################################
    # Token Export
    ###########################################################################

    def export_token_json(
        self,
        mint: str,
    ):

        return self.tokens.export_token(mint)

    ###########################################################################

    def export_token_csv(
        self,
        mint: str,
    ):

        return self.tokens.export_token(mint)

    ###########################################################################

    def export_token_pdf(
        self,
        mint: str,
    ):

        return self.tokens.export_token(mint)

    ###########################################################################
    # Graph Export
    ###########################################################################

    def export_graph_json(
        self,
        graph_id: str,
    ):

        return self.graphs.export_graph(graph_id)

    ###########################################################################

    def export_graph_gexf(
        self,
        graph_id: str,
    ):

        return self.graphs.export_graph(graph_id)

    ###########################################################################

    def export_graph_graphml(
        self,
        graph_id: str,
    ):

        return self.graphs.export_graph(graph_id)

    ###########################################################################

    def export_graph_png(
        self,
        graph_id: str,
    ):

        return self.graphs.export_graph(graph_id)

    ###########################################################################
    # Statistics Export
    ###########################################################################

    def export_statistics(self):

        return self.statistics.export_statistics()

    ###########################################################################

    def export_dashboard(self):

        return self.statistics.export_dashboard()

    ###########################################################################

    def export_report(self):

        return {
            "generated_at": datetime.utcnow().isoformat(),
            "statistics": self.export_statistics(),
        }

    ###########################################################################
    # Bulk Export
    ###########################################################################

    def export_everything(self):

        return {
            "statistics": self.export_statistics(),
            "dashboard": self.export_dashboard(),
        }

    ###########################################################################

    def archive(self):

        payload = json.dumps(
            self.export_everything(),
            default=str,
        )

        return compress(payload)

    ###########################################################################
    # Health
    ###########################################################################

    def health(self):

        return {
            "status": "healthy",
        }

    ###########################################################################

    def diagnostics(self):

        return {
            "repository": "ExportRepository",
            "healthy": self.health(),
        }


###############################################################################
# Runtime
###############################################################################


def summary():

    return {
        "repository": "ExportRepository",
    }


###############################################################################
# Utilities
###############################################################################


def export_filename(
    prefix: str,
    extension: str,
):

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

    return f"{prefix}_{timestamp}.{extension}"


###############################################################################


def compress(
    data: str,
):

    return gzip.compress(
        data.encode("utf-8")
    )


###############################################################################


def checksum(
    data: bytes,
):

    return hashlib.sha256(data).hexdigest()


###############################################################################


def metadata():

    return {
        "module": "ExportRepository",
        "version": "1.0.0",
    }