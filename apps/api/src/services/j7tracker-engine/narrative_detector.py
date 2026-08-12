class NarrativeDetector:

    def detect(

        self,

        mentions,

        growth
    ):

        score = (

            mentions * 0.6 +

            growth * 0.4
        )

        return round(score)