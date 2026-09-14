from __future__ import annotations

from typing import Any

from config.settings import get_settings

from chains.models import (
    Chain,
    ChainAdapter,
    ChainConfig,
)
from trading.jupiter_router import JupiterRouter


class SolanaChainAdapter:
    def __init__(
        self,
        config: ChainConfig,
    ) -> None:
        self.config = config

        settings = get_settings()

        self.jupiter = JupiterRouter(
            api_key=settings.JUPITER_API_KEY,
        )

    async def health(self) -> dict[str, Any]:
        return {
            "chain": Chain.SOLANA.value,
            "status": "configured",
        }

    async def quote(
        self,
        input_token: str,
        output_token: str,
        amount: str,
        wallet: str | None = None,
        slippage_bps: int = 50,
    ) -> dict[str, Any]:
        return await self.jupiter.order(
            input_mint=input_token,
            output_mint=output_token,
            amount=amount,
            taker=wallet,
            slippage_bps=slippage_bps,
        )

    async def build_swap(
        self,
        input_token: str,
        output_token: str,
        amount: str,
        wallet: str,
        slippage_bps: int,
        priority_fee: int | None = None,
        jito_tip: int | None = None,
    ) -> dict[str, Any]:
        return await self.jupiter.order(
            input_mint=input_token,
            output_mint=output_token,
            amount=amount,
            taker=wallet,
            slippage_bps=slippage_bps,
        )

    async def execute(
        self,
        signed_transaction: str,
        request_id: str,
    ) -> dict[str, Any]:
        return await self.jupiter.execute(
            signed_transaction=signed_transaction,
            request_id=request_id,
        )