class StopLossEngine:

    def calculate(

        self,

        entry,

        percent
    ):

        return round(

            entry *

            (1 - percent / 100),

            8
        )