class WalletClassifier:

    def classify(
        self,
        win_rate: float,
        avg_roi: float,
        total_trades: int,
        insider_flags: int
    ):

        if insider_flags > 3:
            return "INSIDER"

        if (
            win_rate >= 70
            and avg_roi >= 3
            and total_trades >= 20
        ):
            return "SMART_MONEY"

        if (
            avg_roi >= 10
            and total_trades >= 5
        ):
            return "DEGEN"

        if (
            total_trades > 500
        ):
            return "WHALE"

        return "RETAIL"