class RiskScore:

    def calculate(

        self,

        mint_risk,

        freeze_risk,

        bundle_risk,

        sniper_risk,

        insider_risk,

        lp_risk
    ):

        total = (

            mint_risk +

            freeze_risk +

            bundle_risk +

            sniper_risk +

            insider_risk +

            lp_risk
        )

        return min(
            100,
            round(total / 6)
        )