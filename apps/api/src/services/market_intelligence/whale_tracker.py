class WhaleTracker:

    def analyze(
        self,
        whale_inflow_usd
    ):

        if whale_inflow_usd > 50000:

            return {

                "signal": "ACCUMULATION",

                "strength": 100
            }

        if whale_inflow_usd > 20000:

            return {

                "signal": "MODERATE",

                "strength": 70
            }

        return {

            "signal": "WEAK",

            "strength": 30
        }