class WalletFlowRanker:

    def rank(

        self,

        smart_money,

        whale_strength,

        fresh_wallets
    ):

        score = (

            smart_money * 0.4 +

            whale_strength * 0.4 +

            fresh_wallets * 0.2
        )

        return round(score)