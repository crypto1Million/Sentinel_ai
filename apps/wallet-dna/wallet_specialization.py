from collections import Counter


class WalletSpecialization:

    def detect(
        self,
        trades: list
    ):

        categories = []

        for trade in trades:

            categories.append(
                trade.get(
                    "category",
                    "UNKNOWN"
                )
            )

        if not categories:

            return []

        counter = Counter(
            categories
        )

        return [
            category
            for category, count
            in counter.most_common(3)
        ]