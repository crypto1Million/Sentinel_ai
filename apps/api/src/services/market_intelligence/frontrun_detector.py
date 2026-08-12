from typing import List, Dict


class FrontRunDetector:

    def detect(
        self,
        transactions: List[Dict]
    ):

        frontrunners = []

        for tx in transactions:

            seconds_before_pump = tx.get(
                "seconds_before_pump",
                9999
            )

            if seconds_before_pump <= 60:

                frontrunners.append(
                    {
                        "wallet":
                        tx["wallet"],

                        "seconds":
                        seconds_before_pump,

                        "amount":
                        tx.get(
                            "amount",
                            0
                        )
                    }
                )

        return {

            "count":
            len(
                frontrunners
            ),

            "wallets":
            frontrunners
        }

    def score(
        self,
        count: int
    ):

        return min(
            count * 10,
            100
        )