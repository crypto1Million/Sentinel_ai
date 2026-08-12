class RealizedPnLTracker:

    def calculate(

        self,

        sell_price,

        cost_basis,

        amount

    ):

        pnl = (sell_price - cost_basis) * amount

        roi = 0

        if cost_basis > 0:

            roi = (

                (sell_price - cost_basis)

                / cost_basis

            ) * 100

        return {

            "realized_pnl": pnl,

            "roi": round(roi, 2)

        }