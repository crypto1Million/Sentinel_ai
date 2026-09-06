class LiquidityFlowEngine:

    def calculate(
        self,
        previous_liquidity: float,
        current_liquidity: float,
    ) -> dict:

        delta = current_liquidity - previous_liquidity

        if previous_liquidity <= 0:
            change_percent = 0.0
        else:
            change_percent = (
                delta / previous_liquidity
            ) * 100

        return {
            "delta_usd": delta,
            "change_percent": change_percent,
            "positive": delta > 0,
        }