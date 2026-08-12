class HolderChurnAnalyzer:

    def analyze(

        self,

        previous_holders,

        current_holders

    ):

        previous = set(previous_holders)

        current = set(current_holders)

        left = previous - current

        joined = current - previous

        churn = 0

        if previous:

            churn = len(left) / len(previous) * 100

        return {

            "previous": len(previous),

            "current": len(current),

            "left": len(left),

            "joined": len(joined),

            "churn_rate": round(churn, 2)

        }