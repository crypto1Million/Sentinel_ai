from typing import List, Dict


class RealizedPnL:

    def calculate(
        self,
        trades: List[Dict]
    ) -> float:

        pnl = 0

        avg_entry = {}

        for trade in trades:

            token = trade["token"]

            if token not in avg_entry:

                avg_entry[token] = trade["price"]

            if trade["side"] == "SELL":

                pnl += (

                    trade["price"]

                    -

                    avg_entry[token]

                ) * trade["amount"]

        return round(
            pnl,
            2
        )