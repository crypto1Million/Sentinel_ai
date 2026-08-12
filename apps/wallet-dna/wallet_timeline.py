from collections import defaultdict


class WalletTimeline:

    def build(
        self,
        trades: list
    ):

        timeline = defaultdict(list)

        for trade in trades:

            date = trade["date"]

            timeline[date].append({

                "token":
                trade["token"],

                "roi":
                trade["roi"]

            })

        return dict(timeline)