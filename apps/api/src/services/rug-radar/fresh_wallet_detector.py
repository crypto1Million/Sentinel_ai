class FreshWalletDetector:

    def analyze(
        self,
        fresh_wallet_percent: float
    ):

        return {

            "fresh_wallet_percent":
            fresh_wallet_percent,

            "quality":

            "HIGH"
            if fresh_wallet_percent > 35
            else "MEDIUM"
        }