from dataclasses import dataclass
from typing import Optional


@dataclass
class FlowSnapshot:
    smart_money_flow: float = 0.0
    liquidity_flow: float = 0.0
    volume_flow: float = 0.0

    smart_money_acceleration: float = 0.0
    liquidity_acceleration: float = 0.0
    volume_acceleration: float = 0.0

    timestamp: Optional[float] = None