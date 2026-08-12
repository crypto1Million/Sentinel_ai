class OpportunityExplainer:

    def analyze(
        self,
        token
    ):

        opportunities = []

        if token["smart_money"] > 15:

            opportunities.append(
                "Smart money accumulation"
            )

        if token["fresh_wallets"] > 30:

            opportunities.append(
                "Fresh wallet growth"
            )

        if token["j7_score"] > 80:

            opportunities.append(
                "Strong J7 activity"
            )

        return opportunities