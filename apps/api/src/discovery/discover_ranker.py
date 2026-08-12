class DiscoverRanker:

    def rank(
        self,
        sentinel_score: float,
        volume_growth: float,
        wallet_quality: float,
        narrative_momentum: float
    ):

        score = (

            sentinel_score * 0.50 +

            volume_growth * 0.15 +

            wallet_quality * 0.20 +

            narrative_momentum * 0.15
        )

        return round(score, 2)