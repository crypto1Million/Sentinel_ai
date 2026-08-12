class VerdictEngine:

    def generate(
        self,
        score: float,
        rug_risk: float
    ):

        if score >= 85 and rug_risk <= 25:
            return "STRONG BUY"

        if score >= 70:
            return "BUY"

        if score >= 50:
            return "WATCH"

        return "AVOID"