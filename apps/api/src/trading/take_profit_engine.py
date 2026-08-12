class TakeProfitEngine:

    def targets(
        self,
        entry
    ):

        return {

            "2x":
            entry * 2,

            "5x":
            entry * 5,

            "10x":
            entry * 10
        }