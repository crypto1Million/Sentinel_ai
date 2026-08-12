from typing import List, Dict


class MEVActivityTracker:

    def analyze(
        self,
        transactions: List[Dict]
    ) -> Dict:

        mev_wallets = []

        for tx in transactions:

            rapid_trades = tx.get(
                "rapid_trades",
                0
            )

            average_hold_time = tx.get(
                "hold_time_seconds",
                999999
            )

            if (

                rapid_trades >= 10

                and

                average_hold_time <= 120

            ):

                mev_wallets.append(
                    {
                        "wallet":
                        tx["wallet"],

                        "rapid_trades":
                        rapid_trades,

                        "hold_time":
                        average_hold_time
                    }
                )

        return {

            "mev_wallets":
            mev_wallets,

            "count":
            len(
                mev_wallets
            )
        }

    def risk_score(
        self,
        count: int
    ):

        return min(
            count * 8,
            100
        )