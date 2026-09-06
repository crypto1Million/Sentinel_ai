from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional


@dataclass(slots=True)
class ClosedTrade:
    trade_id: str
    token_mint: str
    token_name: str
    token_symbol: str

    entry_price: Decimal
    exit_price: Decimal

    position_size_sol: Decimal
    quantity: Decimal

    entry_market_cap: Optional[Decimal] = None
    exit_market_cap: Optional[Decimal] = None

    opened_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None

    token_image_url: Optional[str] = None
    trader_handle: Optional[str] = None

    entry_tx_signature: Optional[str] = None
    exit_tx_signature: Optional[str] = None


@dataclass(slots=True)
class PNLResult:
    pnl_sol: Decimal
    pnl_usd: Optional[Decimal]
    roi_percent: Decimal
    duration_seconds: Optional[int]


@dataclass(slots=True)
class PNLCardData:
    trade_id: str
    token_mint: str
    token_name: str
    token_symbol: str

    pnl_sol: Decimal
    pnl_usd: Optional[Decimal]
    roi_percent: Decimal

    entry_market_cap: Optional[Decimal]
    exit_market_cap: Optional[Decimal]

    position_size_sol: Decimal
    duration_seconds: Optional[int]

    token_image_url: Optional[str]
    trader_handle: Optional[str]

    card_type: str
    generated_at: datetime