from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP
from typing import Optional

from .pnl_card_schema import ClosedTrade, PNLResult


MONEY_PLACES = Decimal("0.000001")
PERCENT_PLACES = Decimal("0.01")


def _quantize_money(value: Decimal) -> Decimal:
    return value.quantize(
        MONEY_PLACES,
        rounding=ROUND_HALF_UP,
    )


def _quantize_percent(value: Decimal) -> Decimal:
    return value.quantize(
        PERCENT_PLACES,
        rounding=ROUND_HALF_UP,
    )


def calculate_realized_pnl(
    trade: ClosedTrade,
    sol_usd_price: Optional[Decimal] = None,
) -> PNLResult:
    """
    Calculate realized PNL from the closed trade.

    pnl_sol = exit value - entry value
    """

    entry_value_sol = (
        trade.entry_price * trade.quantity
    )

    exit_value_sol = (
        trade.exit_price * trade.quantity
    )

    pnl_sol = _quantize_money(
        exit_value_sol - entry_value_sol
    )

    if entry_value_sol == 0:
        roi_percent = Decimal("0")
    else:
        roi_percent = (
            pnl_sol
            / entry_value_sol
            * Decimal("100")
        )

    roi_percent = _quantize_percent(
        roi_percent
    )

    pnl_usd: Optional[Decimal] = None

    if sol_usd_price is not None:
        pnl_usd = _quantize_money(
            pnl_sol * sol_usd_price
        )

    duration_seconds: Optional[int] = None

    if (
        trade.opened_at is not None
        and trade.closed_at is not None
    ):
        duration_seconds = max(
            0,
            int(
                (
                    trade.closed_at
                    - trade.opened_at
                ).total_seconds()
            ),
        )

    return PNLResult(
        pnl_sol=pnl_sol,
        pnl_usd=pnl_usd,
        roi_percent=roi_percent,
        duration_seconds=duration_seconds,
    )