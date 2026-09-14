from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ExecutionMode(str, Enum):
    AUTO = "auto"
    FAST = "fast"
    VERY_FAST = "very_fast"
    MAX = "max"
    CUSTOM = "custom"


@dataclass(frozen=True)
class ExecutionOptions:
    slippage_bps: int
    priority_fee: int | None
    jito_tip: int | None
    mode: ExecutionMode


def validate_execution_options(
    *,
    slippage_bps: int,
    priority_fee: int | None,
    jito_tip: int | None,
    mode: ExecutionMode,
) -> ExecutionOptions:
    if not 1 <= slippage_bps <= 10_000:
        raise ValueError(
            "slippage_bps must be between 1 and 10000"
        )

    if priority_fee is not None:
        if priority_fee < 0:
            raise ValueError(
                "priority_fee cannot be negative"
            )

    if jito_tip is not None:
        if jito_tip < 0:
            raise ValueError(
                "jito_tip cannot be negative"
            )

    return ExecutionOptions(
        slippage_bps=slippage_bps,
        priority_fee=priority_fee,
        jito_tip=jito_tip,
        mode=mode,
    )