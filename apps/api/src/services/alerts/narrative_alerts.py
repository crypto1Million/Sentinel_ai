from typing import Dict, List


class NarrativeAlerts:

    def check(
        self,
        token_data: Dict
    ) -> List[Dict]:

        alerts = []

        momentum = token_data.get(
            "narrative_momentum",
            0
        )

        if momentum >= 80:

            alerts.append({

                "type":
                "NARRATIVE",

                "severity":
                "HIGH",

                "title":
                "Narrative Surge",

                "message":
                "Narrative gaining momentum"

            })

        return alerts