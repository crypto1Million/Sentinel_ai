from typing import List, Dict

from services.alerts.whale_alerts import WhaleAlerts
from services.alerts.smart_money_alerts import SmartMoneyAlerts
from services.alerts.rug_alerts import RugAlerts
from services.alerts.narrative_alerts import NarrativeAlerts
from services.alerts.opportunity_alerts import OpportunityAlerts


class AlertEngine:

    def __init__(self):

        self.whale = WhaleAlerts()

        self.smart_money = SmartMoneyAlerts()

        self.rug = RugAlerts()

        self.narrative = NarrativeAlerts()

        self.opportunity = OpportunityAlerts()

    def analyze(
        self,
        token_data: Dict
    ) -> List[Dict]:

        alerts = []

        alerts.extend(
            self.whale.check(token_data)
        )

        alerts.extend(
            self.smart_money.check(token_data)
        )

        alerts.extend(
            self.rug.check(token_data)
        )

        alerts.extend(
            self.narrative.check(token_data)
        )

        alerts.extend(
            self.opportunity.check(token_data)
        )

        return alerts