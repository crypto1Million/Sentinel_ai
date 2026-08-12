###############################################################################
# Imports
###############################################################################

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

###############################################################################
# Base Model
###############################################################################


class TokenBase(BaseModel):
    """
    Base token model.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )


###############################################################################
# Token
###############################################################################


class Token(TokenBase):
    mint: str
    symbol: str
    name: str
    decimals: int = 9
    supply: Decimal = Decimal("0")
    creator: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


###############################################################################
# TokenSummary
###############################################################################


class TokenSummary(TokenBase):
    mint: str
    symbol: str
    market_cap: float
    liquidity: float
    holders: int
    score: float


###############################################################################
# TokenStatistics
###############################################################################


class TokenStatistics(TokenBase):
    volume_24h: float
    buys_24h: int
    sells_24h: int
    holder_count: int
    transaction_count: int
    updated_at: datetime | None = None


###############################################################################
# TokenHolder
###############################################################################


class TokenHolder(TokenBase):
    wallet: str
    balance: Decimal
    percentage: float
    rank: int


###############################################################################
# TokenTransaction
###############################################################################


class TokenTransaction(TokenBase):
    signature: str
    wallet: str
    side: str
    amount: Decimal
    value_usd: float
    timestamp: datetime


###############################################################################
# TokenFunding
###############################################################################


class TokenFunding(TokenBase):
    source_wallet: str
    destination_wallet: str
    amount_sol: float
    signature: str
    timestamp: datetime


###############################################################################
# TokenScore
###############################################################################


class TokenScore(TokenBase):
    overall: float
    liquidity: float
    holders: float
    narrative: float
    smart_money: float
    rug_risk: float
    ai_confidence: float


###############################################################################
# TokenGraph
###############################################################################


class TokenGraph(TokenBase):
    nodes: list[dict] = Field(default_factory=list)
    edges: list[dict] = Field(default_factory=list)


###############################################################################
# Utilities
###############################################################################


def token_summary(
    token: Token,
) -> dict[str, Any]:
    """
    Serialize token model.
    """

    return token.model_dump()


###############################################################################


def empty_token(
    mint: str,
) -> Token:
    """
    Create empty token model.
    """

    return Token(
        mint=mint,
        symbol="UNKNOWN",
        name="Unknown Token",
    )