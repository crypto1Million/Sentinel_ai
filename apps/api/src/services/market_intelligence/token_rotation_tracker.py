from typing import Dict, List


class TokenRotationTracker:

    def detect_rotation(
        self,
        wallet_activity: List[Dict]
    ) -> Dict:

        rotation_map = {}

        for tx in wallet_activity:

            sold = tx.get(
                "sold_token"
            )

            bought = tx.get(
                "bought_token"
            )

            if not sold or not bought:
                continue

            key = (
                sold,
                bought
            )

            rotation_map[key] = (
                rotation_map.get(
                    key,
                    0
                )
                + 1
            )

        ranked = sorted(
            rotation_map.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return {
            "rotations":
            ranked
        }

    def strongest_rotation(
        self,
        wallet_activity: List[Dict]
    ):

        data = self.detect_rotation(
            wallet_activity
        )

        if not data["rotations"]:
            return None

        return data[
            "rotations"
        ][0]