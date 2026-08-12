class ArbitrageDetector:

    def detect(self, routes):

        opportunities = []

        for route in routes:

            profit = route["output"] - route["input"]

            if profit > 0:

                opportunities.append({

                    "route": route["route"],

                    "profit": profit,

                    "token": route["token"]

                })

        return opportunities

    def total_profit(self, routes):

        return sum(

            x["profit"]

            for x in self.detect(routes)

        )