"""
Mock DexScreener Integration
============================

Fake market-data provider for Sentinel AI tests.
"""

from __future__ import annotations

from typing import Any, Dict


class MockDexScreener:

    def __init__(self):

        self.tokens: Dict[str, Dict[str, Any]] = {}

    # ------------------------------------------------------------------
    # Market Data
    # ------------------------------------------------------------------

    def add_token(
        self,
        mint: str,
        price: float,
        liquidity: float,
        volume_24h: float,
        market_cap: float,
    ):

        data = {
            "mint": mint,
            "price": price,
            "liquidity": liquidity,
            "volume_24h": volume_24h,
            "market_cap": market_cap,
        }

        self.tokens[mint] = data

        return data

    def get_token(
        self,
        mint: str,
    ):

        return self.tokens.get(mint)

    def get_price(
        self,
        mint: str,
    ):

        token = self.get_token(mint)

        return token["price"] if token else 0.0

    def get_liquidity(
        self,
        mint: str,
    ):

        token = self.get_token(mint)

        return token["liquidity"] if token else 0.0

    def get_volume(
        self,
        mint: str,
    ):

        token = self.get_token(mint)

        return token["volume_24h"] if token else 0.0

    def get_market_cap(
        self,
        mint: str,
    ):

        token = self.get_token(mint)

        return token["market_cap"] if token else 0.0

    # ------------------------------------------------------------------
    # Runtime
    # ------------------------------------------------------------------

    def diagnostics(self):

        return {
            "connected": True,
            "tokens": len(self.tokens),
        }

    def summary(self):

        return {
            "service": "mock-dexscreener",
            "tokens": len(self.tokens),
        }


def mock_dexscreener() -> MockDexScreener:

    dexscreener = MockDexScreener()

    dexscreener.add_token(
        mint="TOKEN001",
        price=0.0012,
        liquidity=125_000,
        volume_24h=850_000,
        market_cap=1_200_000,
    )

    dexscreener.add_token(
        mint="TOKEN002",
        price=0.00031,
        liquidity=45_000,
        volume_24h=120_000,
        market_cap=310_000,
    )

    return dexscreener