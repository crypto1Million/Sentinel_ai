from __future__ import annotations

from decimal import Decimal
from typing import Any

from chains.models import Chain
from chains.router import get_chain_adapter

from revenue.fee_policy import FeePolicy

from trading.execution_options import (
    ExecutionMode,
    validate_execution_options,
)


class TradeExecutor:
    def __init__(
        self,
        fee_policy: FeePolicy | None = None,
    ) -> None:
        self.fee_policy = (
            fee_policy
            or FeePolicy()
        )

    async def quote(
        self,
        *,
        chain: Chain,
        input_token: str,
        output_token: str,
        amount: str,
        wallet: str | None,
        slippage_bps: int,
    ) -> dict[str, Any]:
        adapter = get_chain_adapter(chain)

        result = await adapter.quote(
            input_token=input_token,
            output_token=output_token,
            amount=amount,
            wallet=wallet,
            slippage_bps=slippage_bps,
        )

        return {
            "chain": chain.value,
            "quote": result,
        }

    async def build_swap(
        self,
        *,
        chain: Chain,
        input_token: str,
        output_token: str,
        amount: str,
        wallet: str,
        slippage_bps: int,
        priority_fee: int | None,
        jito_tip: int | None,
        execution_mode: ExecutionMode,
        notional_usd: str,
    ) -> dict[str, Any]:
        execution = validate_execution_options(
            slippage_bps=slippage_bps,
            priority_fee=priority_fee,
            jito_tip=jito_tip,
            mode=execution_mode,
        )

        fee_policy = self.fee_policy.evaluate(
            chain=chain,
            notional_usd=Decimal(
                notional_usd
            ),
        )

        adapter = get_chain_adapter(chain)

        transaction = await adapter.build_swap(
            input_token=input_token,
            output_token=output_token,
            amount=amount,
            wallet=wallet,
            slippage_bps=(
                execution.slippage_bps
            ),
            priority_fee=(
                execution.priority_fee
            ),
            jito_tip=execution.jito_tip,
        )

        return {
            "chain": chain.value,
            "wallet": wallet,
            "platform_fee": {
                "bps": (
                    fee_policy
                    .platform_fee
                    .fee_bps
                ),
                "percent": str(
                    fee_policy
                    .platform_fee
                    .fee_percent
                ),
                "notional_usd": str(
                    fee_policy
                    .platform_fee
                    .notional_usd
                ),
                "fee_amount_usd": str(
                    fee_policy
                    .platform_fee
                    .fee_amount_usd
                ),
                "fee_asset": (
                    fee_policy.fee_asset
                ),
            },
            "execution": {
                "mode": execution.mode.value,
                "slippage_bps": (
                    execution.slippage_bps
                ),
                "priority_fee": (
                    execution.priority_fee
                ),
                "jito_tip": execution.jito_tip,
            },
            "transaction": transaction,
        }

    async def execute_signed(
        self,
        *,
        chain: Chain,
        signed_transaction: str,
        request_id: str,
    ) -> dict[str, Any]:
        adapter = get_chain_adapter(chain)

        return await adapter.execute(
            signed_transaction=signed_transaction,
            request_id=request_id,
        )