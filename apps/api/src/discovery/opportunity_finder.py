class OpportunityFinder:

    def find(
        self,
        token
    ):

        conditions = [

            token["sentinel_score"] >= 80,

            token["wallet_quality"] >= 70,

            token["rug_risk"] <= 30,

            token["narrative_momentum"] >= 70
        ]

        return all(conditions)