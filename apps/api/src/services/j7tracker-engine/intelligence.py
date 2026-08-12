from j7_score import J7Score

class J7Intelligence:

    def __init__(self):

        self.score = J7Score()

    def analyze(
        self,
        data
    ):

        j7_score = self.score.calculate(

            data["follows"],

            data["deploys"],

            data["mentions"]
        )

        return {

            "j7_score":
            j7_score,

            "narrative":
            data["narrative"],

            "confidence":

            "HIGH"

            if j7_score > 80

            else "MEDIUM"
        }