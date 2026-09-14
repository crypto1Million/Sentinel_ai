from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class FeeTier:
    minimum_notional_usd: Decimal
    fee_bps: int


@dataclass(frozen=True)
class PlatformFeeResult:
    notional_usd: Decimal
    fee_bps: int
    fee_percent: Decimal
    fee_amount_usd: Decimal


DEFAULT_TIERS: tuple[FeeTier, ...] = (
    FeeTier(
        minimum_notional_usd=Decimal("0"),
        fee_bps=50,
    ),
    FeeTier(
        minimum_notional_usd=Decimal("1000"),
        fee_bps=55,
    ),
    FeeTier(
        minimum_notional_usd=Decimal("10000"),
        fee_bps=60,
    ),
    FeeTier(
        minimum_notional_usd=Decimal("50000"),
        fee_bps=65,
    ),
    FeeTier(
        minimum_notional_usd=Decimal("250000"),
        fee_bps=75,
    ),
)


class PlatformFeeEngine:
    def __init__(
        self,
        tiers: tuple[FeeTier, ...] = DEFAULT_TIERS,
    ) -> None:
        if not tiers:
            raise ValueError(
                "At least one fee tier is required"
            )

        ordered = sorted(
            tiers,
            key=lambda tier:
                tier.minimum_notional_usd,
        )

        self.tiers = tuple(ordered)

    def resolve_fee_bps(
        self,
        notional_usd: Decimal,
    ) -> int:
        if notional_usd < 0:
            raise ValueError(
                "Trade notional cannot be negative"
            )

        selected = self.tiers[0]

        for tier in self.tiers:
            if (
                notional_usd
                >= tier.minimum_notional_usd
            ):
                selected = tier
            else:
                break

        return selected.fee_bps

    def calculate(
        self,
        notional_usd: Decimal,
    ) -> PlatformFeeResult:
        fee_bps = self.resolve_fee_bps(
            notional_usd
        )

        fee_amount = (
            notional_usd
            * Decimal(fee_bps)
            / Decimal("10000")
        )

        return PlatformFeeResult(
            notional_usd=notional_usd,
            fee_bps=fee_bps,
            fee_percent=(
                Decimal(fee_bps)
                / Decimal("100")
            ),
            fee_amount_usd=fee_amount,
        )