class NarrativeMomentumScorer:

    def calculate(
        self,
        narrative_rank: int,
        narrative_growth: float,
        narrative_volume_growth: float
    ):

        score = 0

        score += max(
            0,
            40 - narrative_rank
        )

        score += min(
            narrative_growth,
            30
        )

        score += min(
            narrative_volume_growth,
            30
        )

        return max(
            0,
            min(score, 100)
        )