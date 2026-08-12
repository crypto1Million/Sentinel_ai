class InfluenceScore:

    def calculate(

        self,

        followers,

        engagement
    ):

        score = (

            followers * 0.4 +

            engagement * 0.6
        )

        return min(
            100,
            round(score)
        )