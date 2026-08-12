"""
Helius Client
=============

Official client used to communicate with the Helius APIs.
"""

###############################################################################
# Imports
###############################################################################

from __future__ import annotations

from typing import Any, Dict, List, Optional

import requests

###############################################################################
# Helius Client
###############################################################################


class HeliusClient:
    """
    Main Helius API Client.
    """

    ###########################################################################
    # Initialization
    ###########################################################################

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://mainnet.helius-rpc.com",
        timeout: int = 30,
    ):

        self.api_key = api_key

        self.base_url = base_url.rstrip("/")

        self.timeout = timeout

        self.session = requests.Session()

    ###########################################################################

    def connect(self):

        self.session.headers.update(
            self.headers()
        )

        return True

    ###########################################################################

    def disconnect(self):

        self.session.close()

    ###########################################################################

    def health(self):

        try:

            response = self.raw_rpc(
                "getHealth",
                [],
            )

            return {
                "healthy": response is not None,
            }

        except Exception:

            return {
                "healthy": False,
            }

    ###########################################################################
    # RPC
    ###########################################################################

    def get_account(
        self,
        wallet: str,
    ):

        return self.raw_rpc(
            "getAccountInfo",
            [wallet],
        )

    ###########################################################################

    def get_transaction(
        self,
        signature: str,
    ):

        return self.raw_rpc(
            "getTransaction",
            [signature],
        )

    ###########################################################################

    def get_token_accounts(
        self,
        wallet: str,
    ):

        return self.raw_rpc(
            "getTokenAccountsByOwner",
            [wallet],
        )

    ###########################################################################

    def get_assets(
        self,
        owner: str,
    ):

        endpoint = self.build_url(
            "/v0/addresses/{}/assets".format(owner)
        )

        return self.request(
            "GET",
            endpoint,
        )

    ###########################################################################

    def get_signatures(
        self,
        wallet: str,
    ):

        return self.raw_rpc(
            "getSignaturesForAddress",
            [wallet],
        )

    ###########################################################################

    def get_balance(
        self,
        wallet: str,
    ):

        return self.raw_rpc(
            "getBalance",
            [wallet],
        )

    ###########################################################################

    def get_token_metadata(
        self,
        mint: str,
    ):

        endpoint = self.build_url(
            "/v0/token-metadata"
        )

        return self.request(
            "POST",
            endpoint,
            json={
                "mintAccounts": [mint],
            },
        )

    ###########################################################################

    def raw_rpc(
        self,
        method: str,
        params: Optional[List[Any]] = None,
    ):

        endpoint = (
            f"{self.base_url}/?api-key={self.api_key}"
        )

        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params or [],
        }

        return self.request(
            "POST",
            endpoint,
            json=payload,
        )

    ###########################################################################
    # Enhanced APIs
    ###########################################################################

    def enhanced_transaction(
        self,
        signature: str,
    ):

        endpoint = self.build_url(
            f"/v0/transactions/{signature}"
        )

        return self.request(
            "GET",
            endpoint,
        )

    ###########################################################################

    def parsed_transaction(
        self,
        signature: str,
    ):

        return self.enhanced_transaction(
            signature,
        )

    ###########################################################################

    def wallet_history(
        self,
        wallet: str,
    ):

        endpoint = self.build_url(
            f"/v0/addresses/{wallet}/transactions"
        )

        return self.request(
            "GET",
            endpoint,
        )

    ###########################################################################

    def token_history(
        self,
        mint: str,
    ):

        endpoint = self.build_url(
            f"/v0/token-history/{mint}"
        )

        return self.request(
            "GET",
            endpoint,
        )

    ###########################################################################

    def asset_search(
        self,
        query: Dict[str, Any],
    ):

        endpoint = self.build_url(
            "/v0/search-assets"
        )

        return self.request(
            "POST",
            endpoint,
            json=query,
        )

    ###########################################################################
    # Runtime
    ###########################################################################

    def diagnostics(self):

        return {
            "base_url": self.base_url,
            "connected": self.session is not None,
            "timeout": self.timeout,
        }

    ###########################################################################

    def summary(self):

        return {
            "provider": "Helius",
            "base_url": self.base_url,
        }

    ###########################################################################
    # Utilities
    ###########################################################################

    def headers(self):

        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    ###########################################################################

    def build_url(
        self,
        endpoint: str,
    ):

        endpoint = endpoint.lstrip("/")

        return (
            f"https://api.helius.xyz/{endpoint}"
            f"?api-key={self.api_key}"
        )

    ###########################################################################

    def request(
        self,
        method: str,
        url: str,
        **kwargs,
    ):

        response = self.session.request(
            method=method,
            url=url,
            timeout=self.timeout,
            **kwargs,
        )

        response.raise_for_status()

        return response.json()