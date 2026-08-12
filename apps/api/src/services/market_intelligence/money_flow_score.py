class MoneyFlowScore:

    def calculate(

        self,

        smart_money,

        inflow,

        outflow,

        whales
    ):

        net_flow = max(
            inflow - outflow,
            0
        )

        score = (

            smart_money * 0.3 +

            whales * 0.3 +

            net_flow * 0.4
        )

        return min(
            100,
            round(score)
        )