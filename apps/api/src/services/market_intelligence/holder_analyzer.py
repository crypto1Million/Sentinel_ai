class HolderAnalyzer:

    def analyze(

        self,

        holder_growth,

        unique_holders
    ):

        score = (

            holder_growth * 0.6 +

            unique_holders * 0.4
        )

        return round(score)