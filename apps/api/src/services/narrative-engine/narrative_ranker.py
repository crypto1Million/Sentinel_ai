class NarrativeRanker:

    def rank(
        self,
        narrative_strength: int,
        mentions: int,
        growth: float
    ):

        score = (

            narrative_strength * 0.5 +

            mentions * 0.3 +

            growth * 0.2
        )

        return round(score, 2)