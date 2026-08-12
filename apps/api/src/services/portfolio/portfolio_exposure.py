from collections import defaultdict


class PortfolioExposure:

    def calculate(
        self,
        positions
    ):

        exposure = defaultdict(float)

        for p in positions:

            exposure[
                p["sector"]
            ] += p["value"]

        return dict(exposure)