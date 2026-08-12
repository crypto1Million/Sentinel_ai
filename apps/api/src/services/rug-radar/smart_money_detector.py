class SmartMoneyDetector:

    def analyze(
        self,
        smart_money_percent: float
    ):

        return {

            "smart_money_percent":
            smart_money_percent,

            "strength":

            "HIGH"
            if smart_money_percent > 15
            else "LOW"
        }