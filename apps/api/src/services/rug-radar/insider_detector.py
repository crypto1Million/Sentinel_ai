class InsiderDetector:

    def detect(
        self,
        insider_percent: float
    ):

        if insider_percent > 20:

            return {

                "risk": "HIGH",

                "score": 100
            }

        if insider_percent > 10:

            return {

                "risk": "MEDIUM",

                "score": 50
            }

        return {

            "risk": "LOW",

            "score": 0
        }