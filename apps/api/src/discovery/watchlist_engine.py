class WatchlistEngine:

    def generate(
        self,
        tokens
    ):

        return sorted(

            tokens,

            key=lambda x:
            x["sentinel_score"],

            reverse=True
        )[:50]