###############################################################################
# Imports
###############################################################################

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

###############################################################################
# Base Model
###############################################################################


class BundleBase(BaseModel):
    """
    Base bundle model.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )


###############################################################################
# Bundle
###############################################################################


class Bundle(BundleBase):
    bundle_id: str
    token: str
    deployer: str | None = None
    wallet_count: int = 0
    created_at: datetime
    updated_at: datetime | None = None


###############################################################################
# BundleWallet
###############################################################################


class BundleWallet(BundleBase):
    wallet: str
    allocation_percent: float
    rank: int
    insider: bool = False
    sniper: bool = False


###############################################################################
# BundleStatistics
###############################################################################


class BundleStatistics(BundleBase):
    bundle_count: int
    wallet_count: int
    average_wallets: float
    average_allocation: float
    suspicious_bundles: int
    updated_at: datetime


###############################################################################
# BundleScore
###############################################################################


class BundleScore(BundleBase):
    overall: float
    concentration: float
    decentralization: float
    insider_risk: float
    sniper_risk: float
    rug_probability: float
    ai_confidence: float


###############################################################################
# BundleGraph
###############################################################################


class BundleGraph(BundleBase):
    nodes: list[dict[str, Any]] = Field(default_factory=list)
    edges: list[dict[str, Any]] = Field(default_factory=list)


###############################################################################
# Utilities
###############################################################################


def bundle_summary(
    bundle: Bundle,
) -> dict[str, Any]:
    """
    Serialize bundle.
    """

    return bundle.model_dump()


###############################################################################


def empty_bundle() -> Bundle:
    """
    Create empty bundle.
    """

    return Bundle(
        bundle_id="",
        token="",
        created_at=datetime.utcnow(),
    )