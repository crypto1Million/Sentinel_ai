from datetime import datetime
from typing import List, Dict


class DormantWalletWakeup:

    def detect(
        self,
        wallets: List[Dict],
        dormant_days: int = 30
    ) -> List[Dict]:

        awakened = []

        now = datetime.utcnow()

        for wallet in wallets:

            last_tx = wallet.get("last_transaction")

            if not last_tx:
                continue

            inactive_days = (
                now - last_tx
            ).days

            if inactive_days >= dormant_days:

                awakened.append(
                    {
                        "wallet": wallet["wallet"],
                        "inactive_days": inactive_days,
                        "current_action":
                        wallet.get(
                            "current_action",
                            "UNKNOWN"
                        ),
                        "value":
                        wallet.get(
                            "value",
                            0
                        )
                    }
                )

        return awakened

    def calculate_wakeup_score(
        self,
        awakened_wallets: List[Dict]
    ) -> int:

        score = len(
            awakened_wallets
        ) * 5

        return min(score, 100)