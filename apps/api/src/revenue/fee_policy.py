from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from chains.models import Chain
from revenue.platform_fee import (
    PlatformFeeEngine,
    PlatformFeeResult,
)


@dataclass(frozen=True)
class FeePolicyResult:
    platform_fee: PlatformFeeResult
    fee_asset: str


class FeePolicy:
    def __init__(
        self,
        engine: PlatformFeeEngine | None = None,
    ) -> None:
        self.engine = (
            engine
            or PlatformFeeEngine()
        )

    def evaluate(
        self,
        *,
        chain: Chain,
        notional_usd: Decimal,
    ) -> FeePolicyResult:
        result = self.engine.calculate(
            notional_usd
        )

        fee_asset = (
            "SOL"
            if chain == Chain.SOLANA
            else "NATIVE"
        )

        return FeePolicyResult(
            platform_fee=result,
            fee_asset=fee_asset,
        )