class WalletQualityScorer:

    def calculate(
        self,
        smart_money_count: int,
        whale_count: int,
        insider_count: int
    ):

        score = 0

        score += smart_money_count * 12

        score += whale_count * 5

        score -= insider_count * 20

        return max(
            0,
            min(score, 100)
        )