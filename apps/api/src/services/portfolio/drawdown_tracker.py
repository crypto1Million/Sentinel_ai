class DrawdownTracker:

    def calculate(
        self,
        equity_curve
    ):

        peak = equity_curve[0]

        max_drawdown = 0

        for value in equity_curve:

            peak = max(
                peak,
                value
            )

            drawdown = (

                peak - value

            ) / peak

            max_drawdown = max(
                max_drawdown,
                drawdown
            )

        return round(
            max_drawdown * 100,
            2
        )