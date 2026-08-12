class InflowOutflow:

    def analyze(

        self,

        inflow,

        outflow
    ):

        net_flow = (

            inflow - outflow
        )

        return {

            "net_flow":
            net_flow,

            "bullish":
            net_flow > 0
        }