class ConvictionEngine:

    def classify(
        self,
        sentinel_score: float
    ):

        if sentinel_score >= 90:
            return "EXTREME"

        if sentinel_score >= 80:
            return "HIGH"

        if sentinel_score >= 65:
            return "MEDIUM"

        return "LOW"