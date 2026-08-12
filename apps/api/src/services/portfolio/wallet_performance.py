class WalletPerformance:

    def calculate(
        self,
        pnl,
        starting_balance
    ):

        if starting_balance == 0:

            return 0

        return round(

            (pnl / starting_balance)

            * 100,

            2
        )