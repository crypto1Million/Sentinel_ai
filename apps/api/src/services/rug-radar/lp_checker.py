class LPChecker:

    def analyze(
        self,
        lp_burned: bool
    ):

        return {

            "lp_burned":
            lp_burned,

            "risk":
            0 if lp_burned else 80
        }