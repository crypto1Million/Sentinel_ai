from typing import Dict, List
from collections import defaultdict


class NarrativeCapitalFlow:

    def analyze(
        self,
        tokens: List[Dict]
    ) -> Dict:

        narrative_flows = defaultdict(float)

        for token in tokens:

            narrative = token.get(
                "narrative",
                "unknown"
            )

            volume = token.get(
                "volume_24h",
                0
            )

            narrative_flows[
                narrative
            ] += volume

        sorted_flows = sorted(
            narrative_flows.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return {
            "rankings":
            sorted_flows,
            "leader":
            sorted_flows[0][0]
            if sorted_flows
            else None
        }

    def momentum_score(
        self,
        current_volume: float,
        previous_volume: float
    ):

        if previous_volume <= 0:
            return 100

        growth = (
            (
                current_volume
                - previous_volume
            )
            /
            previous_volume
        ) * 100

        return round(
            growth,
            2
        )