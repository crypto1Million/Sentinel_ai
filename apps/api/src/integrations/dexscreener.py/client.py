"""
DexScreener Client
==================

Official client for interacting with the DexScreener REST API.
"""

###############################################################################
# Imports
###############################################################################

from __future__ import annotations

from typing import Any, Dict, List

import requests

###############################################################################
# DexScreenerClient
###############################################################################


class DexScreenerClient:
    """
    DexScreener API Client.
    """

    ###########################################################################
    # Initialization
    ###########################################################################

    def __init__(
        self,
        base_url: str = "https://api.dexscreener.com/latest",
        timeout: int = 30,
    ):

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

            self.request(
                "GET",
                self.build_url("/dex/search?q=SOL"),
            )

            return {
                "healthy": True,
            }

        except Exception:

            return {
                "healthy": False,
            }

    ###########################################################################
    # Pair APIs
    ###########################################################################

    def get_pair(
        self,
        chain: str,
        pair_address: str,
    ):

        return self.request(
            "GET",
            self.build_url(
                f"/dex/pairs/{chain}/{pair_address}"
            ),
        )

    ###########################################################################

    def get_pairs(
        self,
        pair_addresses: List[str],
    ):

        addresses = ",".join(pair_addresses)

        return self.request(
            "GET",
            self.build_url(
                f"/dex/pairs/solana/{addresses}"
            ),
        )

    ###########################################################################

    def latest_pairs(self):

        return self.request(
            "GET",
            self.build_url(
                "/dex/latest"
            ),
        )

    ###########################################################################

    def trending_pairs(self):

        return self.request(
            "GET",
            self.build_url(
                "/dex/trending"
            ),
        )

    ###########################################################################

    def pair_by_address(
        self,
        address: str,
    ):

        return self.request(
            "GET",
            self.build_url(
                f"/dex/search?q={address}"
            ),
        )

    ###########################################################################
    # Token APIs
    ###########################################################################

    def token_info(
        self,
        token: str,
    ):

        return self.search(token)

    ###########################################################################

    def token_pairs(
        self,
        token: str,
    ):

        return self.request(
            "GET",
            self.build_url(
                f"/dex/tokens/{token}"
            ),
        )

    ###########################################################################

    def token_price(
        self,
        token: str,
    ):

        data = self.token_pairs(token)

        return data

    ###########################################################################

    def token_chart(
        self,
        token: str,
    ):

        return self.token_pairs(token)

    ###########################################################################

    def token_liquidity(
        self,
        token: str,
    ):

        return self.token_pairs(token)

    ###########################################################################
    # Search APIs
    ###########################################################################

    def search(
        self,
        query: str,
    ):

        return self.request(
            "GET",
            self.build_url(
                f"/dex/search?q={query}"
            ),
        )

    ###########################################################################

    def search_symbol(
        self,
        symbol: str,
    ):

        return self.search(symbol)

    ###########################################################################

    def search_name(
        self,
        name: str,
    ):

        return self.search(name)

    ###########################################################################

    def raw_request(
        self,
        endpoint: str,
    ):

        return self.request(
            "GET",
            self.build_url(endpoint),
        )

    ###########################################################################
    # Runtime
    ###########################################################################

    def diagnostics(self):

        return {
            "provider": "DexScreener",
            "base_url": self.base_url,
            "timeout": self.timeout,
        }

    ###########################################################################

    def summary(self):

        return {
            "provider": "DexScreener",
            "status": "ready",
        }

    ###########################################################################
    # Utilities
    ###########################################################################

    def headers(self):

        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "SentinelAI",
        }

    ###########################################################################

    def build_url(
        self,
        endpoint: str,
    ):

        return (
            f"{self.base_url}/{endpoint.lstrip('/')}"
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