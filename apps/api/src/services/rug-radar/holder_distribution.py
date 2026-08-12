class HolderDistribution:

    def analyze(
        self,
        top10_percent: float
    ):

        if top10_percent > 60:

            return "CONCENTRATED"

        if top10_percent > 35:

            return "MODERATE"

        return "HEALTHY"