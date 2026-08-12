class RugRiskScorer:

    def calculate(
        self,
        mint_enabled: bool,
        freeze_enabled: bool,
        dev_wallet_percent: float,
        bundled_wallets: int
    ):

        score = 100

        if mint_enabled:
            score -= 40

        if freeze_enabled:
            score -= 25

        score -= dev_wallet_percent

        score -= bundled_wallets * 5

        return max(
            0,
            min(score, 100)
        )