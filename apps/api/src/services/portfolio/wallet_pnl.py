class WalletPnL:

    def calculate(
        self,
        realized_pnl: float,
        unrealized_pnl: float
    ) -> float:

        return round(
            realized_pnl +
            unrealized_pnl,
            2
        )