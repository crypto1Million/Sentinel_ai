class OpportunityScoreScorer:

    def calculate(
        self,
        market_cap: float,
        age_minutes: int,
        score_boost: float
    ):

        score = 100

        if market_cap > 100000:
            score -= 15

        if market_cap > 500000:
            score -= 20

        if market_cap > 1000000:
            score -= 20

        if age_minutes > 1440:
            score -= 20

        score += score_boost

        return max(
            0,
            min(score, 100)
        )