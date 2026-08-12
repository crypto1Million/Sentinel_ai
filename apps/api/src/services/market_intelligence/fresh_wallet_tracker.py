class FreshWalletTracker:

    def analyze(
        self,
        fresh_percent
    ):

        return {

            "fresh_wallets":
            fresh_percent,

            "score":
            min(
                100,
                fresh_percent * 2
            )
        }