"""
Raydium Models
==============

Pydantic models for Raydium Integration.
"""

###############################################################################
# Imports
###############################################################################

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field

###############################################################################
# Models
###############################################################################


class TokenModel(BaseModel):

    mint: str

    symbol: Optional[str] = None

    name: Optional[str] = None

    decimals: int = 9


###############################################################################


class PoolModel(BaseModel):

    id: str

    base_token: TokenModel

    quote_token: TokenModel

    liquidity_usd: float = 0

    tvl: float = 0

    status: Optional[str] = None


###############################################################################


class SwapModel(BaseModel):

    input_token: str

    output_token: str

    input_amount: float

    output_amount: float

    minimum_received: float = 0

    price_impact: float = 0

    signature: Optional[str] = None


###############################################################################


class LiquidityModel(BaseModel):

    pool: str

    base_amount: float = 0

    quote_amount: float = 0

    lp_supply: float = 0

    usd_value: float = 0


###############################################################################


class APRModel(BaseModel):

    apr: float = 0

    farm_apr: float = 0

    trading_apr: float = 0


###############################################################################


class FeeModel(BaseModel):

    swap_fee: float = 0

    protocol_fee: float = 0


###############################################################################


class VolumeModel(BaseModel):

    volume_24h: float = Field(default=0)

    volume_7d: float = Field(default=0)

    volume_30d: float = Field(default=0)


###############################################################################


class PositionModel(BaseModel):

    wallet: str

    pool: str

    lp_tokens: float = 0

    share: float = 0

    usd_value: float = 0


###############################################################################
# Runtime
###############################################################################


def summary():

    return {
        "models": [
            "PoolModel",
            "TokenModel",
            "SwapModel",
            "LiquidityModel",
            "APRModel",
            "FeeModel",
            "VolumeModel",
            "PositionModel",
        ]
    }


###############################################################################
# Utilities
###############################################################################


def validators():

    return {
        "pool": "base58",
        "mint": "base58",
        "wallet": "base58",
        "signature": "base58",
    }