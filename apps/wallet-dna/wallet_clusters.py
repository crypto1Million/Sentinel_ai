from collections import defaultdict


class WalletClusterEngine:

    def cluster(
        self,
        wallet_trades: list
    ):

        clusters = defaultdict(list)

        for trade in wallet_trades:

            token = trade["mint"]

            clusters[token].append(
                trade["wallet"]
            )

        return dict(clusters)