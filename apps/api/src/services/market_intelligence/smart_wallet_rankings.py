from typing import List, Dict


class SmartWalletRankings:

    def rank(
        self,
        wallets: List[Dict]
    ) -> List[Dict]:

        ranked = []

        for wallet in wallets:

            score = (
                wallet.get("win_rate", 0) * 0.35
                + wallet.get("roi", 0) * 0.25
                + wallet.get("realized_pnl", 0) * 0.20
                + wallet.get("early_entries", 0) * 0.10
                + wallet.get("conviction_score", 0) * 0.10
            )

            wallet["smart_score"] = round(score, 2)

            ranked.append(wallet)

        ranked.sort(
            key=lambda x: x["smart_score"],
            reverse=True
        )

        return ranked

    def top_wallets(
        self,
        wallets: List[Dict],
        limit: int = 25
    ):

        return self.rank(wallets)[:limit]