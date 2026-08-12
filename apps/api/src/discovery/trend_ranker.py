class TrendRanker:

    def rank(
        self,
        mentions,
        volume_growth,
        holder_growth
    ):

        score = (

            mentions * 0.4 +

            volume_growth * 0.3 +

            holder_growth * 0.3
        )

        return round(score)