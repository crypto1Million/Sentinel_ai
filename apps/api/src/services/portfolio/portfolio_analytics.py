from typing import Dict, List


class PortfolioAnalytics:

    def analyze(
        self,
        positions: List[Dict]
    ) -> Dict:

        total_value = 0

        largest_position = None

        largest_value = 0

        for p in positions:

            value = (

                p["amount"]

                *

                p["current_price"]

            )

            total_value += value

            if value > largest_value:

                largest_value = value

                largest_position = p["token"]

        return {

            "portfolio_value":
            round(total_value, 2),

            "largest_position":
            largest_position,

            "largest_position_value":
            round(largest_value, 2)
        }