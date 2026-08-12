"""
Jupiter Client
==============

Official Jupiter REST API client for Sentinel AI.
"""

###############################################################################
# Imports
###############################################################################

from __future__ import annotations

from typing import Any, Dict, Optional

import requests

###############################################################################
# JupiterClient
###############################################################################


class JupiterClient:
    """
    Jupiter Aggregator REST Client.
    """

    ###########################################################################
    # Initialization
    ###########################################################################

    def __init__(
        self,
        base_url: str = "https://quote-api.jup.ag/v6",
        timeout: int = 30,
    ):

        self.base_url = base_url.rstrip("/")

        self.timeout = timeout

        self.session = requests.Session()

    ###########################################################################

    def connect(self) -> bool:

        self.session.headers.update(
            self.headers()
        )

        return True

    ###########################################################################

    def disconnect(self):

        self.session.close()

    ###########################################################################

    def health(self) -> Dict[str, Any]:

        try:

            self.request(
                "GET",
                self.build_url("/health"),
            )

            return {
                "healthy": True,
            }

        except Exception as exc:

            return {
                "healthy": False,
                "error": str(exc),
            }

    ###########################################################################
    # Quote APIs
    ###########################################################################

    def quote(
        self,
        input_mint: str,
        output_mint: str,
        amount: int,
        slippage_bps: int = 50,
    ):

        return self.request(
            "GET",
            self.build_url("/quote"),
            params={
                "inputMint": input_mint,
                "outputMint": output_mint,
                "amount": amount,
                "slippageBps": slippage_bps,
            },
        )

    ###########################################################################

    def quote_exact_out(
        self,
        input_mint: str,
        output_mint: str,
        amount: int,
        slippage_bps: int = 50,
    ):

        return self.request(
            "GET",
            self.build_url("/quote"),
            params={
                "swapMode": "ExactOut",
                "inputMint": input_mint,
                "outputMint": output_mint,
                "amount": amount,
                "slippageBps": slippage_bps,
            },
        )

    ###########################################################################
    # Swap APIs
    ###########################################################################

    def build_swap(
        self,
        payload: Dict,
    ):

        return self.request(
            "POST",
            self.build_url("/swap"),
            json=payload,
        )

    ###########################################################################

    def simulate_swap(
        self,
        payload: Dict,
    ):

        return self.request(
            "POST",
            self.build_url("/swap"),
            json=payload,
        )

    ###########################################################################

    def execute_swap(
        self,
        payload: Dict,
    ):

        return self.request(
            "POST",
            self.build_url("/swap"),
            json=payload,
        )

    ###########################################################################
    # Route APIs
    ###########################################################################

    def routes(
        self,
        input_mint: str,
        output_mint: str,
        amount: int,
    ):

        return self.quote(
            input_mint,
            output_mint,
            amount,
        )

    ###########################################################################

    def best_route(
        self,
        input_mint: str,
        output_mint: str,
        amount: int,
    ):

        return self.quote(
            input_mint,
            output_mint,
            amount,
        )

    ###########################################################################

    def raw_request(
        self,
        endpoint: str,
        method: str = "GET",
        **kwargs,
    ):

        return self.request(
            method,
            self.build_url(endpoint),
            **kwargs,
        )

    ###########################################################################
    # Runtime
    ###########################################################################

    def diagnostics(self):

        return {
            "provider": "Jupiter",
            "base_url": self.base_url,
            "timeout": self.timeout,
        }

    ###########################################################################

    def summary(self):

        return {
            "provider": "Jupiter",
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