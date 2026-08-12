from typing import List, Dict


class UnrealizedPnL:

    def calculate(
        self,
        positions: List[Dict]
    ) -> float:

        pnl = 0

        for position in positions:

            pnl += (

                position["current_price"]

                -

                position["entry_price"]

            ) * position["amount"]

        return round(
            pnl,
            2
        )