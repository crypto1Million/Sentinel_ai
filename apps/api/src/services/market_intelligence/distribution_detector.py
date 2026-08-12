class DistributionDetector:

    def detect(

        self,

        sells,

        buys
    ):

        ratio = sells / max(
            buys,
            1
        )

        if ratio >= 3:

            return "HEAVY"

        if ratio >= 1.5:

            return "MODERATE"

        return "LOW"