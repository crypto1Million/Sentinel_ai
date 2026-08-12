class SmartMoneyTracker:

    def analyze(
        self,
        smart_wallets: int
    ):

        if smart_wallets >= 20:

            return {

                "grade": "A",

                "score": 95
            }

        if smart_wallets >= 10:0

            return {

                "grade": "B",

                "score": 75
            }

        return {

            "grade": "C",

            "score": 50
        }