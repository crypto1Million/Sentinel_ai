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


class WalletBase(BaseModel):
    """
    Base wallet model.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )


###############################################################################
# Wallet
###############################################################################


class Wallet(WalletBase):
    address: str
    first_seen: datetime | None = None
    last_seen: datetime | None = None
    balance_sol: Decimal = Decimal("0")
    transaction_count: int = 0
    label: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


###############################################################################
# WalletSummary
###############################################################################


class WalletSummary(WalletBase):
    address: str
    score: float
    risk: float
    conviction: float
    cluster: str | None = None
    funding_source: str | None = None


###############################################################################
# WalletScore
###############################################################################


class WalletScore(WalletBase):
    overall: float
    conviction: float
    narrative: float
    risk: float
    funding: float
    behaviour: float
    ai_confidence: float


###############################################################################
# WalletStatistics
###############################################################################


class WalletStatistics(WalletBase):
    transactions: int
    unique_tokens: int
    realized_pnl: float
    unrealized_pnl: float
    average_hold_time: float
    win_rate: float
    last_active: datetime | None = None


###############################################################################
# WalletActivity
###############################################################################


class WalletActivity(WalletBase):
    timestamp: datetime
    action: str
    token: str | None = None
    amount: float | None = None
    value_usd: float | None = None
    signature: str | None = None


###############################################################################
# WalletFunding
###############################################################################


class WalletFunding(WalletBase):
    source_wallet: str
    destination_wallet: str
    amount_sol: float
    tx_signature: str
    timestamp: datetime


###############################################################################
# WalletGraph
###############################################################################


class WalletGraph(WalletBase):
    nodes: list[dict] = Field(default_factory=list)
    edges: list[dict] = Field(default_factory=list)


###############################################################################
# WalletTraits
###############################################################################


class WalletTraits(WalletBase):
    sniper: bool = False
    insider: bool = False
    holder: bool = False
    trader: bool = False
    deployer: bool = False
    whale: bool = False
    fresh_wallet: bool = False


###############################################################################
# WalletLabels
###############################################################################


class WalletLabels(WalletBase):
    labels: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    confidence: float = 0.0


###############################################################################
# Utilities
###############################################################################


def wallet_summary(
    wallet: Wallet,
) -> dict[str, Any]:
    """
    Serialize wallet.
    """

    return wallet.model_dump()


###############################################################################


def empty_wallet(
    address: str,
) -> Wallet:
    """
    Create empty wallet object.
    """

    return Wallet(
        address=address,
    )