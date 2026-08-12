class BundleDetector:

    def detect(
        self,
        bundled_percent: float
    ):

        if bundled_percent > 30:

            return {

                "risk": "HIGH",

                "score": 100
            }

        if bundled_percent > 15:

            return {

                "risk": "MEDIUM",

                "score": 50
            }

        return {

            "risk": "LOW",

            "score": 0
        }