class PortfolioRisk:

    def calculate(
        self,
        positions
    ):

        concentration = max(
            [
                p["allocation"]
                for p in positions
            ],
            default=0
        )

        if concentration > 50:

            return "HIGH"

        if concentration > 25:

            return "MEDIUM"

        return "LOW"