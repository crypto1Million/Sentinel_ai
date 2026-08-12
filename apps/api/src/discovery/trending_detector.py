class TrendingDetector:

    def detect(
        self,
        token
    ):

        return (

            token["volume_growth"] > 50

            and

            token["holder_growth"] > 20
        )