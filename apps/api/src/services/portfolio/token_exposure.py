from collections import defaultdict


class TokenExposure:

    def calculate(
        self,
        positions
    ):

        result = defaultdict(float)

        for p in positions:

            result[
                p["token"]
            ] += p["value"]

        return dict(result)