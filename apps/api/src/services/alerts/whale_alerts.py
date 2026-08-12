from typing import Dict, List


class WhaleAlerts:

    def check(
        self,
        token_data: Dict
    ) -> List[Dict]:

        alerts = []

        whale_buys = token_data.get(
            "whale_buys",
            0
        )

        if whale_buys >= 5:

            alerts.append({

                "type": "WHALE",

                "title":
                "Whale Accumulation",

                "severity":
                "HIGH",

                "message":
                f"{whale_buys} whale wallets entered"

            })

        return alerts