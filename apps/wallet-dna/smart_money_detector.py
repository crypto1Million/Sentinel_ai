class SmartMoneyDetector:

    def is_smart_money(
        self,
        win_rate: float,
        avg_roi: float,
        total_trades: int
    ):

        if (
            win_rate >= 75
            and avg_roi >= 3
            and total_trades >= 25
        ):
            return True

        return False

    def confidence_score(
        self,
        win_rate: float,
        avg_roi: float,
        total_trades: int
    ):

        score = 0

        score += min(
            win_rate,
            40
        )

        score += min(
            avg_roi * 5,
            30
        )

        score += min(
            total_trades / 5,
            30
        )

        return min(score, 100)