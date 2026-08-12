class J7Score:

    def calculate(

        self,

        follows,

        deploys,

        mentions
    ):

        return min(

            100,

            follows * 4 +

            deploys * 5 +

            mentions * 2
        )