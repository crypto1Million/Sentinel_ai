class VolumeQualityScorer:

    def calculate(
        self,
        volume_usd: float,
        unique_buyers: int,
        repeated_wallets: int
    ):

        score = 0

        score += min(
            volume_usd / 1000,
            50
        )

        score += min(
            unique_buyers,
            40
        )

        score -= min(
            repeated_wallets * 3,
            40
        )

        return max(
            0,
            min(score, 100)
        )