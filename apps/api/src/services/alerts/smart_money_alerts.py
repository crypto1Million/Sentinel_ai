from typing import Dict, List


class SmartMoneyAlerts:

    def check(
        self,
        token_data: Dict
    ) -> List[Dict]:

        alerts = []

        smart_money = token_data.get(
            "smart_money_percent",
            0
        )

        if smart_money >= 15:

            alerts.append({

                "type": "SMART_MONEY",

                "title":
                "Smart Money Entering",

                "severity":
                "HIGH",

                "message":
                f"{smart_money}% smart money holders"

            })

        return alerts