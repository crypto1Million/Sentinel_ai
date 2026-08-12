from typing import List, Dict


class TradeJournal:

    def summarize(
        self,
        trades: List[Dict]
    ) -> Dict:

        total = len(trades)

        wins = len(
            [
                t for t in trades
                if t.get("pnl", 0) > 0
            ]
        )

        losses = total - wins

        return {
            "total_trades": total,
            "wins": wins,
            "losses": losses,
            "win_rate":
                round(
                    wins / total * 100,
                    2
                )
                if total
                else 0
        }