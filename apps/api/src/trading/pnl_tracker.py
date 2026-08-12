class PnLTracker:

    def calculate(

        self,

        entry,

        current,

        size
    ):

        pnl = (

            current - entry

        ) * size

        return round(
            pnl,
            2
        )