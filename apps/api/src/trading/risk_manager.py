class RiskManager:

    def allow_trade(

        self,

        sentinel_score,

        rug_risk
    ):

        if sentinel_score < 60:

            return False

        if rug_risk > 70:

            return False

        return True