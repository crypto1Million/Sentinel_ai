class DevQualityScorer:

    def calculate(
        self,
        successful_launches: int,
        rugs: int,
        avg_ath_multiple: float,
        wallet_age_days: int
    ):

        score = 50

        score += successful_launches * 5

        score -= rugs * 25

        score += min(
            avg_ath_multiple,
            10
        ) * 2

        score += min(
            wallet_age_days / 30,
            10
        )

        return max(
            0,
            min(score, 100)
        )