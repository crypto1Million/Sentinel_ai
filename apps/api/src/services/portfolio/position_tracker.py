from typing import List, Dict


class PositionTracker:

    def get_open_positions(
        self,
        trades: List[Dict]
    ) -> List[Dict]:

        positions = {}

        for trade in trades:

            token = trade["token"]

            if token not in positions:

                positions[token] = {
                    "token": token,
                    "amount": 0,
                    "cost_basis": 0
                }

            if trade["side"] == "BUY":

                positions[token]["amount"] += trade["amount"]

                positions[token]["cost_basis"] += (
                    trade["amount"] *
                    trade["price"]
                )

            elif trade["side"] == "SELL":

                positions[token]["amount"] -= (
                    trade["amount"]
                )

        return list(
            positions.values()
        )