"""
Pump.fun Client
===============

Client for interacting with the Pump.fun APIs.
"""

###############################################################################
# Imports
###############################################################################

from __future__ import annotations

from typing import Any, Dict, List, Optional

import requests

###############################################################################
# PumpFunClient
###############################################################################


class PumpFunClient:
    """
    Pump.fun API Client.
    """

    ###########################################################################
    # Initialization
    ###########################################################################

    def __init__(
        self,
        base_url: str = "https://frontend-api.pump.fun",
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

            response = self.request(
                "GET",
                self.build_url("/health"),
            )

            return {
                "healthy": response is not None,
            }

        except Exception:

            return {
                "healthy": False,
            }

    ###########################################################################
    # Token APIs
    ###########################################################################

    def get_token(
        self,
        mint: str,
    ):

        return self.request(
            "GET",
            self.build_url(f"/coins/{mint}"),
        )

    ###########################################################################

    def get_tokens(self):

        return self.request(
            "GET",
            self.build_url("/coins"),
        )

    ###########################################################################

    def search_tokens(
        self,
        query: str,
    ):

        return self.request(
            "GET",
            self.build_url(f"/search?q={query}"),
        )

    ###########################################################################

    def latest_tokens(self):

        return self.request(
            "GET",
            self.build_url("/coins/latest"),
        )

    ###########################################################################

    def trending_tokens(self):

        return self.request(
            "GET",
            self.build_url("/coins/trending"),
        )

    ###########################################################################

    def token_metadata(
        self,
        mint: str,
    ):

        return self.request(
            "GET",
            self.build_url(f"/metadata/{mint}"),
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
    # Deployer APIs
    ###########################################################################

    def deployer_tokens(
        self,
        wallet: str,
    ):

        return self.request(
            "GET",
            self.build_url(
                f"/creator/{wallet}/coins"
            ),
        )

    ###########################################################################

    def deployer_history(
        self,
        wallet: str,
    ):

        return self.request(
            "GET",
            self.build_url(
                f"/creator/{wallet}/history"
            ),
        )

    ###########################################################################

    def deployer_statistics(
        self,
        wallet: str,
    ):

        return self.request(
            "GET",
            self.build_url(
                f"/creator/{wallet}/stats"
            ),
        )

    ###########################################################################
    # Bonding Curve
    ###########################################################################

    def bonding_curve(
        self,
        mint: str,
    ):

        return self.request(
            "GET",
            self.build_url(
                f"/bonding-curve/{mint}"
            ),
        )

    ###########################################################################

    def curve_progress(
        self,
        mint: str,
    ):

        return self.request(
            "GET",
            self.build_url(
                f"/bonding-curve/{mint}/progress"
            ),
        )

    ###########################################################################

    def liquidity(
        self,
        mint: str,
    ):

        return self.request(
            "GET",
            self.build_url(
                f"/liquidity/{mint}"
            ),
        )

    ###########################################################################

    def migration_status(
        self,
        mint: str,
    ):

        return self.request(
            "GET",
            self.build_url(
                f"/migration/{mint}"
            ),
        )

    ###########################################################################
    # Runtime
    ###########################################################################

    def diagnostics(self):

        return {
            "provider": "Pump.fun",
            "base_url": self.base_url,
            "timeout": self.timeout,
        }

    ###########################################################################

    def summary(self):

        return {
            "provider": "Pump.fun",
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