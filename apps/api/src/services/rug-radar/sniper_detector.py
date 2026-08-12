class SniperDetector:

    def detect(
        self,
        sniper_percent: float
    ):

        if sniper_percent > 25:

            return {

                "risk": "HIGH",

                "score": 90
            }

        if sniper_percent > 10:

            return {

                "risk": "MEDIUM",

                "score": 45
            }

        return {

            "risk": "LOW",

            "score": 0
        }