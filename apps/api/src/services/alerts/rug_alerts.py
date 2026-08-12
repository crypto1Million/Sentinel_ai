from typing import Dict, List


class RugAlerts:

    def check(
        self,
        token_data: Dict
    ) -> List[Dict]:

        alerts = []

        bundled = token_data.get(
            "bundled_percent",
            0
        )

        dev = token_data.get(
            "dev_wallet_percent",
            0
        )

        if bundled > 20:

            alerts.append({

                "type": "RUG",

                "severity":
                "CRITICAL",

                "title":
                "High Bundle Risk",

                "message":
                f"{bundled}% bundled supply"

            })

        if dev > 15:

            alerts.append({

                "type": "RUG",

                "severity":
                "HIGH",

                "title":
                "Large Dev Allocation",

                "message":
                f"{dev}% dev wallet"

            })

        return alerts