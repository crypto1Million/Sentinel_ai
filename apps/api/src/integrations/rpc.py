"""
Helius RPC
==========

Low-level Solana JSON-RPC wrapper for Helius.
"""

###############################################################################
# Imports
###############################################################################

from __future__ import annotations

from typing import Any, Dict, List, Optional

import requests

###############################################################################
# HeliusRPC
###############################################################################


class HeliusRPC:
    """
    Low-level RPC interface.
    """

    ###########################################################################
    # Initialization
    ###########################################################################

    def __init__(
        self,
        api_key: str,
        rpc_url: str = "https://mainnet.helius-rpc.com",
        timeout: int = 30,
    ):

        self.api_key = api_key

        self.rpc_url = (
            f"{rpc_url}/?api-key={api_key}"
        )

        self.timeout = timeout

        self.session = requests.Session()

    ###########################################################################
    # RPC Methods
    ###########################################################################

    def get_slot(self):

        return self.raw_rpc(
            "getSlot",
        )

    ###########################################################################

    def get_block(
        self,
        slot: int,
    ):

        return self.raw_rpc(
            "getBlock",
            [slot],
        )

    ###########################################################################

    def get_epoch(self):

        return self.raw_rpc(
            "getEpochInfo",
        )

    ###########################################################################

    def get_supply(self):

        return self.raw_rpc(
            "getSupply",
        )

    ###########################################################################

    def get_vote_accounts(self):

        return self.raw_rpc(
            "getVoteAccounts",
        )

    ###########################################################################

    def get_cluster_nodes(self):

        return self.raw_rpc(
            "getClusterNodes",
        )

    ###########################################################################

    def send_transaction(
        self,
        transaction: str,
    ):

        return self.raw_rpc(
            "sendTransaction",
            [transaction],
        )

    ###########################################################################

    def simulate_transaction(
        self,
        transaction: str,
    ):

        return self.raw_rpc(
            "simulateTransaction",
            [transaction],
        )

    ###########################################################################

    def raw_rpc(
        self,
        method: str,
        params: Optional[List[Any]] = None,
    ):

        payload = rpc_payload(
            method,
            params,
        )

        response = self.session.post(
            self.rpc_url,
            json=payload,
            headers=rpc_headers(),
            timeout=self.timeout,
        )

        response.raise_for_status()

        return response.json()

    ###########################################################################
    # Runtime
    ###########################################################################

    def diagnostics(self):

        return {
            "rpc_url": self.rpc_url,
            "timeout": self.timeout,
            "connected": True,
        }

    ###########################################################################

    def summary(self):

        return {
            "provider": "Helius RPC",
            "endpoint": self.rpc_url,
        }


###############################################################################
# Utilities
###############################################################################


def rpc_payload(
    method: str,
    params: Optional[List[Any]] = None,
) -> Dict:

    return {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params or [],
    }


###############################################################################


def rpc_headers():

    return {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }