class LiquidityChecker:

    def check(
        self,
        liquidity_usd: float
    ):

        if liquidity_usd >= 100000:
            return "HIGH"

        if liquidity_usd >= 25000:
            return "MEDIUM"

        return "LOW"