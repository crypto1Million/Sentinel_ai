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


class FundingBase(BaseModel):
    """
    Base funding model.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )


###############################################################################
# FundingChain
###############################################################################


class FundingChain(FundingBase):
    chain_id: str
    source_wallet: str
    destination_wallet: str
    amount_sol: Decimal
    depth: int
    signature: str
    timestamp: datetime


###############################################################################
# FundingNode
###############################################################################


class FundingNode(FundingBase):
    wallet: str
    balance_sol: Decimal = Decimal("0")
    label: str | None = None
    score: float | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


###############################################################################
# FundingEdge
###############################################################################


class FundingEdge(FundingBase):
    source: str
    destination: str
    amount_sol: Decimal
    signature: str
    timestamp: datetime
    weight: float = 1.0


###############################################################################
# FundingStatistics
###############################################################################


class FundingStatistics(FundingBase):
    chain_count: int
    node_count: int
    edge_count: int
    average_depth: float
    maximum_depth: int
    suspicious_chains: int
    updated_at: datetime


###############################################################################
# FundingScore
###############################################################################


class FundingScore(FundingBase):
    overall: float
    trust_score: float
    source_quality: float
    chain_complexity: float
    laundering_risk: float
    ai_confidence: float


###############################################################################
# Utilities
###############################################################################


def funding_summary(
    chain: FundingChain,
) -> dict[str, Any]:
    """
    Serialize funding chain.
    """

    return chain.model_dump()


###############################################################################


def empty_funding_chain() -> FundingChain:
    """
    Create empty funding chain.
    """

    return FundingChain(
        chain_id="",
        source_wallet="",
        destination_wallet="",
        amount_sol=Decimal("0"),
        depth=0,
        signature="",
        timestamp=datetime.utcnow(),
    )