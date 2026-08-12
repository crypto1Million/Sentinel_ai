from typing import List, Dict


class LiquidityMigration:

    def detect(
        self,
        source_token: str,
        destination_token: str,
        wallets: List[Dict]
    ) -> Dict:

        migrated_wallets = []
        migrated_value = 0

        for wallet in wallets:

            sold = wallet.get(
                "sold_source",
                0
            )

            bought = wallet.get(
                "bought_destination",
                0
            )

            if sold > 0 and bought > 0:

                migrated_wallets.append(
                    wallet["wallet"]
                )

                migrated_value += min(
                    sold,
                    bought
                )

        return {
            "source": source_token,
            "destination": destination_token,
            "wallets": len(
                migrated_wallets
            ),
            "value": migrated_value,
            "migration_strength":
            round(
                migrated_value /
                max(
                    len(
                        migrated_wallets
                    ),
                    1
                ),
                2
            )
        }