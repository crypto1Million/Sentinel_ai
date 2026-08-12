class AccumulationDetector:

    def detect(

        self,

        buys,

        sells
    ):

        ratio = buys / max(
            sells,
            1
        )

        if ratio >= 3:

            return "STRONG"

        if ratio >= 1.5:

            return "MODERATE"

        return "WEAK"