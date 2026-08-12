"""
Pump.fun Models
===============

Pydantic models for Pump.fun API responses.
"""

###############################################################################
# Imports
###############################################################################

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field

###############################################################################
# Pump.fun Models
###############################################################################


class TokenModel(BaseModel):

    mint: str

    name: Optional[str] = None

    symbol: Optional[str] = None

    creator: Optional[str] = None

    market_cap: Optional[float] = None

    volume: Optional[float] = None

    liquidity: Optional[float] = None

    verified: bool = False


###############################################################################


class LaunchModel(BaseModel):

    mint: str

    creator: str

    created_at: Optional[str] = None

    market_cap: Optional[float] = None

    volume: Optional[float] = None

    liquidity: Optional[float] = None

    migrated: bool = False


###############################################################################


class DeployerModel(BaseModel):

    wallet: str

    total_launches: int = 0

    successful_launches: int = 0

    rug_count: int = 0

    trust_score: Optional[float] = None


###############################################################################


class BondingCurveModel(BaseModel):

    progress: float = 0.0

    virtual_sol: float = 0.0

    virtual_token: float = 0.0

    completed: bool = False


###############################################################################


class LiquidityModel(BaseModel):

    liquidity: float = 0.0

    locked: bool = False

    burned: bool = False


###############################################################################


class HolderModel(BaseModel):

    wallet: str

    balance: float

    percentage: float


###############################################################################


class TransactionModel(BaseModel):

    signature: str

    wallet: str

    side: Optional[str] = None

    amount: float = 0.0

    timestamp: Optional[str] = None


###############################################################################


class MigrationModel(BaseModel):

    migrated: bool = False

    destination: Optional[str] = None

    migration_time: Optional[str] = None


###############################################################################
# Runtime
###############################################################################


def summary():

    return {
        "models": [
            "TokenModel",
            "LaunchModel",
            "DeployerModel",
            "BondingCurveModel",
            "LiquidityModel",
            "HolderModel",
            "TransactionModel",
            "MigrationModel",
        ]
    }


###############################################################################
# Utilities
###############################################################################


def validators():

    return {
        "wallet": "base58",
        "mint": "base58",
        "creator": "base58",
    }