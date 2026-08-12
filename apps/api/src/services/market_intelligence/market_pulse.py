class MarketPulse:

    def generate(

        self,

        money_flow_score,

        holder_growth
    ):

        if (

            money_flow_score > 80

            and

            holder_growth > 20
        ):

            return "BULLISH"

        if money_flow_score > 60:

            return "NEUTRAL"

        return "BEARISH"