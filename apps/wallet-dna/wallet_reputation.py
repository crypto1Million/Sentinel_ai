class WalletReputation:

    def calculate(
        self,
        wallet_age_days: int,
        win_rate: float,
        avg_roi: float,
        rug_count: int
    ):

        score = 50

        score += min(
            wallet_age_days / 30,
            20
        )

        score += min(
            win_rate / 2,
            20
        )

        score += min(
            avg_roi * 2,
            20
        )

        score -= rug_count * 15

        return max(
            0,
            min(score, 100)
        )