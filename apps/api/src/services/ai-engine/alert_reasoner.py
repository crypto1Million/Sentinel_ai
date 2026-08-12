class AlertReasoner:

    def analyze(
        self,
        previous_score,
        current_score
    ):

        delta = current_score - previous_score

        if delta >= 20:

            return "Major bullish shift"

        if delta <= -20:

            return "Major bearish shift"

        return "Neutral"