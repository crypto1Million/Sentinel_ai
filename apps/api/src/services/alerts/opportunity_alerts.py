from typing import Dict, List


class OpportunityAlerts:

    def check(
        self,
        token_data: Dict
    ) -> List[Dict]:

        alerts = []

        score = token_data.get(
            "sentinel_score",
            0
        )

        rug_risk = token_data.get(
            "rug_risk",
            100
        )

        if score >= 85 and rug_risk <= 20:

            alerts.append({

                "type":
                "OPPORTUNITY",

                "severity":
                "HIGH",

                "title":
                "High Conviction Opportunity",

                "message":
                "Strong Sentinel setup detected"

            })

        return alerts