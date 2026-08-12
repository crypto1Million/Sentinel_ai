class RecommendationEngine:

    def generate(
        self,
        verdict,
        confidence
    ):

        if verdict == "STRONG BUY":

            return (
                "Aggressive accumulation "
                "possible."
            )

        if verdict == "BUY":

            return (
                "Consider scaling in."
            )

        if verdict == "WATCH":

            return (
                "Monitor before entry."
            )

        return (
            "Avoid current setup."
        )