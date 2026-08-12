from typing import List, Dict


class ExitLiquidityDetector:

    def detect(
        self,
        trades: List[Dict]
    ) -> Dict:

        suspicious_wallets = []

        for trade in trades:

            early_entry = trade.get(
                "entry_mc",
                0
            )

            exit_mc = trade.get(
                "exit_mc",
                0
            )

            profit_multiple = (
                exit_mc /
                max(
                    early_entry,
                    1
                )
            )

            if profit_multiple >= 10:

                suspicious_wallets.append(
                    {
                        "wallet":
                        trade["wallet"],

                        "entry_mc":
                        early_entry,

                        "exit_mc":
                        exit_mc,

                        "multiple":
                        round(
                            profit_multiple,
                            2
                        )
                    }
                )

        score = min(
            len(
                suspicious_wallets
            ) * 5,
            100
        )

        return {

            "exit_liquidity_score":
            score,

            "wallets":
            suspicious_wallets
        }