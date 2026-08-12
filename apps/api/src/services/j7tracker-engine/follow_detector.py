class FollowDetector:

    def detect(
        self,
        follows: int
    ):

        if follows >= 10:

            return {

                "signal":
                "STRONG",

                "score":
                90
            }

        if follows >= 5:

            return {

                "signal":
                "MEDIUM",

                "score":
                50
            }

        return {

            "signal":
            "LOW",

            "score":
            10
        }