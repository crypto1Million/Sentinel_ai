from collections import defaultdict


class NarrativeExposure:

    def calculate(
        self,
        positions
    ):

        narratives = defaultdict(float)

        for p in positions:

            narratives[
                p["narrative"]
            ] += p["value"]

        return dict(narratives)