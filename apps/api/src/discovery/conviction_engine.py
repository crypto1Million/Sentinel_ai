class ConvictionEngine:

    def classify(
        self,
        score
    ):

        if score >= 90:

            return "EXTREME"

        if score >= 80:

            return "HIGH"

        if score >= 60:

            return "MEDIUM"

        return "LOW"