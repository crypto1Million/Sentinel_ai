class ConfidenceEngine:

    def calculate(
        self,
        score,
        wallet_quality,
        narrative
    ):

        confidence = (

            score * 0.5 +

            wallet_quality * 0.25 +

            narrative * 0.25
        )

        return round(confidence)