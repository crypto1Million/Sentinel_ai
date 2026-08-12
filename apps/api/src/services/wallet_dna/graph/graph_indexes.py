"""
graph_indexes.py

Central index manager for WalletDNA graph engine.
Provides O(1) lookups for wallets, tokens, edges and clusters.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Dict, Set, Optional, List, Any


class GraphIndexes:
    """
    Central registry for every lookup table used by DeployerGraph.

    Purpose:
    ----------
    • Wallet lookup
    • Token lookup
    • Edge lookup
    • Cluster lookup
    • Reverse indexes
    • Fast traversals
    """

    def __init__(self) -> None:

        # ==========================================================
        # NODE INDEXES
        # ==========================================================

        self.wallet_index: Dict[str, Any] = {}

        self.token_index: Dict[str, Any] = {}

        self.node_registry: Dict[str, Any] = {}

        # ==========================================================
        # EDGE INDEXES
        # ==========================================================

        self.funding_index: Dict[str, Set[Any]] = defaultdict(set)

        self.deployment_index: Dict[str, Set[Any]] = defaultdict(set)

        self.transfer_index: Dict[str, Set[Any]] = defaultdict(set)

        self.bundle_index: Dict[str, Set[Any]] = defaultdict(set)

        self.interaction_index: Dict[str, Set[Any]] = defaultdict(set)

        # ==========================================================
        # SOURCE / DESTINATION
        # ==========================================================

        self.source_index: Dict[str, Set[Any]] = defaultdict(set)

        self.destination_index: Dict[str, Set[Any]] = defaultdict(set)

        # ==========================================================
        # CLUSTERS
        # ==========================================================

        self.cluster_index: Dict[int, Set[str]] = defaultdict(set)

        self.reverse_cluster_index: Dict[str, int] = {}

    ####################################################################
    # WALLET METHODS
    ####################################################################

    def register_wallet(self, wallet) -> None:
        self.wallet_index[wallet.address] = wallet
        self.node_registry[wallet.address] = wallet

    def get_wallet(self, address: str):

        return self.wallet_index.get(address)

    def has_wallet(self, address: str) -> bool:

        return address in self.wallet_index

    def remove_wallet(self, address: str) -> None:

        self.wallet_index.pop(address, None)
        self.node_registry.pop(address, None)

    ####################################################################
    # TOKEN METHODS
    ####################################################################

    def register_token(self, token) -> None:

        self.token_index[token.mint] = token
        self.node_registry[token.mint] = token

    def get_token(self, mint: str):

        return self.token_index.get(mint)

    def has_token(self, mint: str) -> bool:

        return mint in self.token_index

    def remove_token(self, mint: str) -> None:

        self.token_index.pop(mint, None)
        self.node_registry.pop(mint, None)

    ####################################################################
    # FUNDING EDGES
    ####################################################################

    def register_funding_edge(self, edge) -> None:

        self.funding_index[edge.source].add(edge)

        self.source_index[edge.source].add(edge)

        self.destination_index[edge.destination].add(edge)

    def funding_edges(self, wallet: str):

        return self.funding_index.get(wallet, set())

    ####################################################################
    # DEPLOYMENT EDGES
    ####################################################################

    def register_deployment_edge(self, edge) -> None:

        self.deployment_index[edge.wallet].add(edge)

    def deployment_edges(self, wallet: str):

        return self.deployment_index.get(wallet, set())

    ####################################################################
    # TRANSFER EDGES
    ####################################################################

    def register_transfer_edge(self, edge) -> None:

        self.transfer_index[edge.source].add(edge)

        self.source_index[edge.source].add(edge)

        self.destination_index[edge.destination].add(edge)

    def transfer_edges(self, wallet: str):

        return self.transfer_index.get(wallet, set())

    ####################################################################
    # BUNDLE EDGES
    ####################################################################

    def register_bundle_edge(self, edge) -> None:

        self.bundle_index[edge.bundle_id].add(edge)

    def bundle_edges(self, bundle_id):

        return self.bundle_index.get(bundle_id, set())

    ####################################################################
    # INTERACTION EDGES
    ####################################################################

    def register_interaction_edge(self, edge) -> None:

        self.interaction_index[edge.wallet].add(edge)

    def interaction_edges(self, wallet):

        return self.interaction_index.get(wallet, set())

    ####################################################################
    # SOURCE LOOKUP
    ####################################################################

    def outgoing_edges(self, node: str):

        return self.source_index.get(node, set())

    ####################################################################
    # DESTINATION LOOKUP
    ####################################################################

    def incoming_edges(self, node: str):

        return self.destination_index.get(node, set())

    ####################################################################
    # CLUSTERS
    ####################################################################

    def register_cluster(
        self,
        cluster_id: int,
        wallets: Set[str]
    ) -> None:

        self.cluster_index[cluster_id] = wallets

        for wallet in wallets:

            self.reverse_cluster_index[wallet] = cluster_id

    def add_wallet_to_cluster(
        self,
        wallet: str,
        cluster_id: int
    ) -> None:

        self.cluster_index[cluster_id].add(wallet)

        self.reverse_cluster_index[wallet] = cluster_id

    def remove_wallet_from_cluster(
        self,
        wallet: str
    ) -> None:

        cluster = self.reverse_cluster_index.get(wallet)

        if cluster is None:
            return

        self.cluster_index[cluster].discard(wallet)

        self.reverse_cluster_index.pop(wallet, None)

    def cluster_of(self, wallet: str):

        return self.reverse_cluster_index.get(wallet)

    def cluster_wallets(self, cluster_id: int):

        return self.cluster_index.get(cluster_id, set())

    ####################################################################
    # UTILITIES
    ####################################################################

    def total_wallets(self):

        return len(self.wallet_index)

    def total_tokens(self):

        return len(self.token_index)

    def total_clusters(self):

        return len(self.cluster_index)

    def clear(self):

        self.__init__()

    def statistics(self):

        return {

            "wallets": len(self.wallet_index),

            "tokens": len(self.token_index),

            "clusters": len(self.cluster_index),

            "funding_indexes": len(self.funding_index),

            "deployment_indexes": len(self.deployment_index),

            "transfer_indexes": len(self.transfer_index),

            "bundle_indexes": len(self.bundle_index),

            "interaction_indexes": len(self.interaction_index),
        }

        