class ExplanationEngine:

    def generate(
        self,
        token
    ):

        reasons = []

        if token["wallet_quality"] > 75:

            reasons.append(
                "Strong wallet quality"
            )

        if token["narrative_momentum"] > 75:

            reasons.append(
                "Narrative accelerating"
            )

        if token["rug_risk"] < 25:

            reasons.append(
                "Low rug risk"
            )

        return reasons