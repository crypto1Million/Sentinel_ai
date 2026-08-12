from collections import Counter


class TrendDetector:

    def detect(
        self,
        tokens: list
    ):

        narratives = []

        for token in tokens:

            if "narrative" in token:

                narratives.append(
                    token["narrative"]
                )

        counts = Counter(
            narratives
        )

        return counts.most_common()