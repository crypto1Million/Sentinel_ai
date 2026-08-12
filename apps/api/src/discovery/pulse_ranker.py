class PulseRanker:

    def rank(
        self,
        age_minutes,
        buys,
        volume
    ):

        score = (

            buys * 0.5 +

            volume * 0.3 +

            max(
                0,
                100 - age_minutes
            ) * 0.2
        )

        return round(score)