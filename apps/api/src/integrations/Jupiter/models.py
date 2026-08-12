"""
Jupiter Models
==============

Pydantic models used throughout the Jupiter integration.
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
    """
    Jupiter Token Model.
    """

    mint: str

    symbol: Optional[str] = None

    name: Optional[str] = None

    decimals: int = 9


###############################################################################


class QuoteModel(BaseModel):
    """
    Quote Response.
    """

    input_mint: str

    output_mint: str

    in_amount: float

    out_amount: float

    price_impact: float = 0

    slippage_bps: int = 50

    route_plan: List[dict] = Field(
        default_factory=list
    )


###############################################################################


class RouteModel(BaseModel):
    """
    Route Information.
    """

    swap_mode: str = "ExactIn"

    market_infos: List[dict] = Field(
        default_factory=list
    )

    route_plan: List[dict] = Field(
        default_factory=list
    )


###############################################################################


class SwapModel(BaseModel):
    """
    Swap Transaction.
    """

    swap_transaction: Optional[str] = None

    signature: Optional[str] = None

    last_valid_block_height: Optional[int] = None

    priority_fee: Optional[int] = None

    status: str = "pending"


###############################################################################


class PlatformFeeModel(BaseModel):
    """
    Platform Fee.
    """

    amount: float = 0

    fee_bps: int = 0


###############################################################################


class SlippageModel(BaseModel):
    """
    Slippage Configuration.
    """

    slippage_bps: int = 50

    maximum_price_impact: float = 5.0


###############################################################################
# Runtime
###############################################################################


def summary():

    return {
        "models": [
            "TokenModel",
            "QuoteModel",
            "RouteModel",
            "SwapModel",
            "PlatformFeeModel",
            "SlippageModel",
        ]
    }


###############################################################################
# Utilities
###############################################################################


def validators():

    return {
        "mint": "base58",
        "transaction": "base64",
        "signature": "base58",
        "fee": "positive",
        "slippage": "0-10000 bps",
    }