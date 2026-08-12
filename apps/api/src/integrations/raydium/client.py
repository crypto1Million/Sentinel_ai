"""
Raydium Client
==============

Official Raydium API client used throughout Sentinel AI.
"""

###############################################################################
# Imports
###############################################################################

from __future__ import annotations

from typing import Any, Dict, List

import requests

###############################################################################
# RaydiumClient
###############################################################################


class RaydiumClient:
    """
    Raydium REST Client.
    """

    ###########################################################################
    # Initialization
    ###########################################################################

    def __init__(
        self,
        base_url: str = "https://api.raydium.io",
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
                self.build_url("/v2/main/pairs"),
            )

            return {
                "healthy": True,
            }

        except Exception:

            return {
                "healthy": False,
            }

    ###########################################################################
    # Pool APIs
    ###########################################################################

    def get_pool(
        self,
        pool_id: str,
    ):

        return self.request(
            "GET",
            self.build_url(
                f"/v2/pool/{pool_id}"
            ),
        )

    ###########################################################################

    def get_pools(self):

        return self.request(
            "GET",
            self.build_url(
                "/v2/main/pairs"
            ),
        )

    ###########################################################################

    def latest_pools(self):

        return self.get_pools()

    ###########################################################################

    def trending_pools(self):

        return self.request(
            "GET",
            self.build_url(
                "/v2/main/pairs"
            ),
        )

    ###########################################################################

    def pool_by_address(
        self,
        address: str,
    ):

        return self.get_pool(address)

    ###########################################################################
    # Token APIs
    ###########################################################################

    def token_info(
        self,
        mint: str,
    ):

        return self.request(
            "GET",
            self.build_url(
                f"/v2/sdk/token/{mint}"
            ),
        )

    ###########################################################################

    def token_pools(
        self,
        mint: str,
    ):

        return self.request(
            "GET",
            self.build_url(
                f"/v2/sdk/pairs/{mint}"
            ),
        )

    ###########################################################################

    def token_price(
        self,
        mint: str,
    ):

        return self.request(
            "GET",
            self.build_url(
                f"/v2/main/price?token={mint}"
            ),
        )

    ###########################################################################

    def token_liquidity(
        self,
        mint: str,
    ):

        return self.token_pools(mint)

    ###########################################################################

    def token_volume(
        self,
        mint: str,
    ):

        return self.token_pools(mint)

    ###########################################################################
    # Swap APIs
    ###########################################################################

    def swap_quote(
        self,
        input_mint: str,
        output_mint: str,
        amount: float,
    ):

        return self.request(
            "GET",
            self.build_url(
                f"/v2/sdk/quote?inputMint={input_mint}&outputMint={output_mint}&amount={amount}"
            ),
        )

    ###########################################################################

    def build_swap(
        self,
        payload: Dict,
    ):

        return self.request(
            "POST",
            self.build_url(
                "/v2/sdk/swap"
            ),
            json=payload,
        )

    ###########################################################################

    def simulate_swap(
        self,
        payload: Dict,
    ):

        return self.request(
            "POST",
            self.build_url(
                "/v2/sdk/simulate"
            ),
            json=payload,
        )

    ###########################################################################

    def execute_swap(
        self,
        payload: Dict,
    ):

        return self.request(
            "POST",
            self.build_url(
                "/v2/sdk/execute"
            ),
            json=payload,
        )

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
            "provider": "Raydium",
            "base_url": self.base_url,
            "timeout": self.timeout,
        }

    ###########################################################################

    def summary(self):

        return {
            "provider": "Raydium",
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