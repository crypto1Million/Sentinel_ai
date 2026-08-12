from collections import defaultdict


class SandwichDetector:

    def detect(self, swaps):

        suspicious = []

        grouped = defaultdict(list)

        for tx in swaps:
            grouped[tx["block"]].append(tx)

        for block, transactions in grouped.items():

            if len(transactions) < 3:
                continue

            for i in range(len(transactions)-2):

                a = transactions[i]
                b = transactions[i+1]
                c = transactions[i+2]

                if (
                    a["wallet"] == c["wallet"]
                    and a["side"] == "BUY"
                    and c["side"] == "SELL"
                    and b["wallet"] != a["wallet"]
                ):

                    suspicious.append({

                        "block": block,

                        "attacker": a["wallet"],

                        "victim": b["wallet"],

                        "token": a["token"]

                    })

        return suspicious

    def score(self, sandwiches):

        return min(len(sandwiches) * 20, 100)