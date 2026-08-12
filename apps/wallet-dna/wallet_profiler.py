from statistics import mean


class WalletProfiler:

    def profile(
        self,
        trades: list
    ):

        if not trades:

            return {
                "win_rate": 0,
                "avg_roi": 0,
                "total_trades": 0
            }

        wins = [
            t for t in trades
            if t["roi"] > 0
        ]

        win_rate = (
            len(wins)
            / len(trades)
        ) * 100

        avg_roi = mean(
            t["roi"]
            for t in trades
        )

        return {

            "win_rate":
            round(win_rate, 2),

            "avg_roi":
            round(avg_roi, 2),

            "total_trades":
            len(trades)
        }