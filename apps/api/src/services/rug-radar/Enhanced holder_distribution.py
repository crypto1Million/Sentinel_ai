class HolderDistribution:

    def analyze(

        self,

        top10_percent: float,

        top25_percent: float
    ):

        concentration = (

            top10_percent * 0.7 +

            top25_percent * 0.3
        )

        if concentration > 70:

            return {

                "risk":
                "HIGH",

                "score":
                100
            }

        if concentration > 50:

            return {

                "risk":
                "MEDIUM",

                "score":
                50
            }

        return {

            "risk":
            "LOW",

            "score":
            0
        }