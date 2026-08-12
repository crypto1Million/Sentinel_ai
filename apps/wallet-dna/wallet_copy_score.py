class WalletCopyScore:

    def calculate(
        self,
        win_rate: float,
        avg_roi: float,
        total_trades: int,
        reputation_score: float
    ):

        score = 0

        score += min(
            win_rate * 0.4,
            40
        )

        score += min(
            avg_roi * 5,
            25
        )

        score += min(
            total_trades / 10,
            15
        )

        score += min(
            reputation_score * 0.2,
            20
        )

        return min(score, 100)