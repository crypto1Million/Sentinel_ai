from collections import defaultdict


class WalletProfitHistory:

    def __init__(self):
        self.history = defaultdict(list)

    def add_trade(
        self,
        wallet: str,
        token: str,
        realized_pnl: float,
        timestamp: int,
    ):

        self.history[wallet].append({

            "token": token,

            "realized_pnl": realized_pnl,

            "timestamp": timestamp

        })

    def get_wallet_history(self, wallet):

        return self.history.get(wallet, [])

    def total_profit(self, wallet):

        return sum(
            x["realized_pnl"]

            for x in self.history.get(wallet, [])
        )

    def win_rate(self, wallet):

        trades = self.history.get(wallet, [])

        if not trades:
            return 0

        wins = len([t for t in trades if t["realized_pnl"] > 0])

        return round(wins / len(trades) * 100, 2)