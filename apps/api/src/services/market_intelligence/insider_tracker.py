class InsiderTracker:

    def analyze(
        self,
        insider_percent
    ):

        if insider_percent > 20:

            return {

                "risk": "HIGH",

                "score": 100
            }

        if insider_percent > 10:

            return {

                "risk": "MEDIUM",

                "score": 60
            }

        return {

            "risk": "LOW",

            "score": 20
        }