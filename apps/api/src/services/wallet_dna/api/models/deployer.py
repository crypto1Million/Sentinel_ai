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


class DeployerBase(BaseModel):
    """
    Base deployer model.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )


###############################################################################
# Deployer
###############################################################################


class Deployer(DeployerBase):
    wallet: str
    label: str | None = None
    first_deployment: datetime | None = None
    last_deployment: datetime | None = None
    total_tokens: int = 0
    active_tokens: int = 0
    created_at: datetime | None = None
    updated_at: datetime | None = None


###############################################################################
# DeployerSummary
###############################################################################


class DeployerSummary(DeployerBase):
    wallet: str
    score: float
    reputation: float
    successful_tokens: int
    rugged_tokens: int
    active_tokens: int


###############################################################################
# DeployerStatistics
###############################################################################


class DeployerStatistics(DeployerBase):
    total_deployments: int
    successful_deployments: int
    failed_deployments: int
    rugged_projects: int
    average_marketcap: float
    average_liquidity: float
    updated_at: datetime


###############################################################################
# DeployerScore
###############################################################################


class DeployerScore(DeployerBase):
    overall: float
    reputation: float
    consistency: float
    rug_risk: float
    holder_quality: float
    liquidity_quality: float
    ai_confidence: float


###############################################################################
# DeployerHistory
###############################################################################


class DeployerHistory(DeployerBase):
    token: str
    mint: str
    launch_time: datetime
    peak_marketcap: float | None = None
    current_marketcap: float | None = None
    status: str
    notes: str | None = None


###############################################################################
# Utilities
###############################################################################


def deployer_summary(
    deployer: Deployer,
) -> dict[str, Any]:
    """
    Serialize deployer.
    """

    return deployer.model_dump()


###############################################################################


def empty_deployer(
    wallet: str = "",
) -> Deployer:
    """
    Create empty deployer object.
    """

    return Deployer(
        wallet=wallet,
    )