class DevWalletChecker:

    def analyze(
        self,
        dev_percent: float
    ):

        if dev_percent >= 20:

            return {
                "risk": "HIGH",
                "score": 100
            }

        if dev_percent >= 10:

            return {
                "risk": "MEDIUM",
                "score": 50
            }

        return {
            "risk": "LOW",
            "score": 0
        }