class TrendingEngine:

    def rank(

        self,

        signal_score,

        influence_score
    ):

        return round(

            signal_score * 0.7 +

            influence_score * 0.3
        )