from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional

from .pnl_calculator import calculate_realized_pnl
from .pnl_card_schema import (
    ClosedTrade,
    PNLCardData,
)


class PNLCardService:

    def __init__(
        self,
        trade_repository=None,
        storage=None,
    ):
        self.trade_repository = trade_repository
        self.storage = storage

    # ------------------------------------------------------------------
    # Card Type
    # ------------------------------------------------------------------

    @staticmethod
    def determine_card_type(
        pnl_sol: Decimal,
        roi_percent: Decimal,
    ) -> str:

        if pnl_sol < 0:
            return "loss"

        if roi_percent >= Decimal("500"):
            return "huge_win"

        if roi_percent >= Decimal("200"):
            return "major_win"

        return "profit"

    # ------------------------------------------------------------------
    # Build Card
    # ------------------------------------------------------------------

    def build_card(
        self,
        trade: ClosedTrade,
        sol_usd_price: Optional[Decimal] = None,
    ) -> PNLCardData:

        pnl = calculate_realized_pnl(
            trade,
            sol_usd_price=sol_usd_price,
        )

        card_type = self.determine_card_type(
            pnl.pnl_sol,
            pnl.roi_percent,
        )

        return PNLCardData(
            trade_id=trade.trade_id,
            token_mint=trade.token_mint,
            token_name=trade.token_name,
            token_symbol=trade.token_symbol,

            pnl_sol=pnl.pnl_sol,
            pnl_usd=pnl.pnl_usd,
            roi_percent=pnl.roi_percent,

            entry_market_cap=trade.entry_market_cap,
            exit_market_cap=trade.exit_market_cap,

            position_size_sol=trade.position_size_sol,
            duration_seconds=pnl.duration_seconds,

            token_image_url=trade.token_image_url,
            trader_handle=trade.trader_handle,

            card_type=card_type,
            generated_at=datetime.now(
                timezone.utc
            ),
        )

    # ------------------------------------------------------------------
    # Generate + Persist
    # ------------------------------------------------------------------

    async def generate_for_closed_trade(
        self,
        trade: ClosedTrade,
        sol_usd_price: Optional[Decimal] = None,
    ) -> PNLCardData:

        card = self.build_card(
            trade,
            sol_usd_price=sol_usd_price,
        )

        if self.trade_repository is not None:

            await self.trade_repository.save_pnl_card(
                card
            )

        return card