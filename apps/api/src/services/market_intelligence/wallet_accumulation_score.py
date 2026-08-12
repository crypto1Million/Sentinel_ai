from dataclasses import dataclass
from typing import List, Dict


@dataclass
class WalletPosition:
    wallet: str
    current_balance: float
    previous_balance: float


class WalletAccumulationScore:

    def __init__(self):
        self.max_score = 100

    def calculate(
        self,
        positions: List[WalletPosition]
    ) -> Dict:

        if not positions:
            return {
                "score": 0,
                "status": "NO_DATA"
            }

        increased = 0
        decreased = 0

        total_change = 0

        for position in positions:

            delta = (
                position.current_balance
                - position.previous_balance
            )

            total_change += delta

            if delta > 0:
                increased += 1
            elif delta < 0:
                decreased += 1

        wallet_count = len(positions)

        accumulation_ratio = increased / wallet_count

        score = min(
            int(accumulation_ratio * 100),
            self.max_score
        )

        if score >= 80:
            status = "HEAVY_ACCUMULATION"
        elif score >= 60:
            status = "ACCUMULATION"
        elif score >= 40:
            status = "NEUTRAL"
        elif score >= 20:
            status = "DISTRIBUTION"
        else:
            status = "HEAVY_DISTRIBUTION"

        return {
            "score": score,
            "status": status,
            "wallets_accumulating": increased,
            "wallets_distributing": decreased,
            "net_change": total_change
        }