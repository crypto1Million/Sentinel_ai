"""
DexScreener Models
==================

Pydantic models for DexScreener API responses.
"""

###############################################################################
# Imports
###############################################################################

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field

###############################################################################
# Models
###############################################################################


class TokenModel(BaseModel):

    address: str

    name: Optional[str] = None

    symbol: Optional[str] = None


###############################################################################


class PriceModel(BaseModel):

    usd: Optional[float] = None

    native: Optional[float] = None


###############################################################################


class LiquidityModel(BaseModel):

    usd: Optional[float] = None

    base: Optional[float] = None

    quote: Optional[float] = None


###############################################################################


class VolumeModel(BaseModel):

    h24: Optional[float] = None

    h6: Optional[float] = None

    h1: Optional[float] = None

    m5: Optional[float] = None


###############################################################################


class HolderModel(BaseModel):

    wallet: str

    amount: Optional[float] = None

    percentage: Optional[float] = None


###############################################################################


class TransactionModel(BaseModel):

    buys: int = 0

    sells: int = 0


###############################################################################


class PairModel(BaseModel):

    pair_address: str

    chain: str

    dex: str

    base_token: TokenModel

    quote_token: TokenModel

    price: PriceModel

    liquidity: LiquidityModel

    volume: VolumeModel

    transactions: TransactionModel

    holders: List[HolderModel] = Field(
        default_factory=list
    )

    fdv: Optional[float] = None

    market_cap: Optional[float] = None

    url: Optional[str] = None


###############################################################################


class SearchModel(BaseModel):

    query: str

    results: List[PairModel] = Field(
        default_factory=list
    )

    total: int = 0


###############################################################################
# Runtime
###############################################################################


def summary():

    return {
        "models": [
            "PairModel",
            "TokenModel",
            "PriceModel",
            "LiquidityModel",
            "VolumeModel",
            "HolderModel",
            "TransactionModel",
            "SearchModel",
        ]
    }


###############################################################################
# Utilities
###############################################################################


def validators():

    return {
        "pair_address": "base58",
        "token_address": "base58",
        "wallet": "base58",
    }