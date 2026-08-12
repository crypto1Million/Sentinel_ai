class CostBasisCalculator:

    def calculate(self, buys):

        total_cost = 0
        total_tokens = 0

        for trade in buys:

            total_cost += trade["price"] * trade["amount"]

            total_tokens += trade["amount"]

        if total_tokens == 0:
            return 0

        return total_cost / total_tokens

    def unrealized_pnl(

        self,

        current_price,

        cost_basis,

        amount

    ):

        return (current_price - cost_basis) * amount