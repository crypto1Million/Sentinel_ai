from typing import List, Dict


class EarlyBuyerDetector:

    def detect(
        self,
        buyers: List[Dict]
    ) -> Dict:

        early_buyers = []

        for buyer in buyers:

            if buyer["entry_mc"] < 50000:

                early_buyers.append(
                    buyer
                )

        return {
            "count": len(
                early_buyers
            ),
            "buyers": early_buyers
        }