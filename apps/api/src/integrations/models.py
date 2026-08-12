"""
Helius Models
=============

Pydantic models for Helius API responses.
"""

###############################################################################
# Imports
###############################################################################

from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

###############################################################################
# Helius Models
###############################################################################


class TransactionModel(BaseModel):

    signature: str

    slot: Optional[int] = None

    timestamp: Optional[int] = None

    fee: Optional[int] = None

    accounts: List[str] = Field(default_factory=list)


###############################################################################


class WalletModel(BaseModel):

    wallet: str

    owner: Optional[str] = None

    balance: Optional[int] = None


###############################################################################


class TokenModel(BaseModel):

    mint: str

    symbol: Optional[str] = None

    name: Optional[str] = None

    decimals: Optional[int] = None


###############################################################################


class AssetModel(BaseModel):

    id: Optional[str] = None

    interface: Optional[str] = None

    content: Optional[Dict[str, Any]] = None

    ownership: Optional[Dict[str, Any]] = None


###############################################################################


class InstructionModel(BaseModel):

    program: Optional[str] = None

    instruction_type: Optional[str] = Field(
        default=None,
        alias="type",
    )

    data: Optional[Dict[str, Any]] = None


###############################################################################


class MetadataModel(BaseModel):

    name: Optional[str] = None

    symbol: Optional[str] = None

    uri: Optional[str] = None

    collection: Optional[str] = None


###############################################################################


class BalanceModel(BaseModel):

    wallet: str

    lamports: int

    sol: float


###############################################################################


class WebSocketEvent(BaseModel):

    event: str

    subscription: Optional[int] = None

    payload: Dict[str, Any] = Field(
        default_factory=dict,
    )


###############################################################################
# Runtime
###############################################################################


def summary():

    return {
        "models": [
            "TransactionModel",
            "WalletModel",
            "TokenModel",
            "AssetModel",
            "InstructionModel",
            "MetadataModel",
            "BalanceModel",
            "WebSocketEvent",
        ]
    }


###############################################################################
# Utilities
###############################################################################


def validators():

    return {
        "wallet": "base58",
        "mint": "base58",
        "signature": "base58",
    }