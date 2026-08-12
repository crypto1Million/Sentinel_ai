from collections import defaultdict


class CoordinatedWalletDetector:

    def detect(self, trades):

        groups = defaultdict(list)

        for trade in trades:
            key = (
                trade["token"],
                round(trade["timestamp"], 1)
            )

            groups[key].append(trade["wallet"])

        suspicious = []

        for key, wallets in groups.items():

            if len(wallets) >= 3:

                suspicious.append({
                    "token": key[0],
                    "timestamp": key[1],
                    "wallets": wallets
                })

        return suspicious