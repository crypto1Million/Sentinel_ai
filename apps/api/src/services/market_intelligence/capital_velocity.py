from typing import Dict


class CapitalVelocity:

    def calculate(
        self,
        volume_24h: float,
        market_cap: float
    ) -> Dict:

        if market_cap <= 0:
            return {
                "velocity": 0
            }

        velocity = volume_24h / market_cap

        return {
            "velocity": round(
                velocity,
                2
            )
        }