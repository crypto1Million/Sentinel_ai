from __future__ import annotations

from launchpads.detectors.solana import (
    SolanaLaunchpadDetector,
)

from launchpads.models import (
    LaunchpadCandidate,
    LaunchpadObservation,
)

authoritative_partner_id="jupiter_studio"

class MeteoraDetector:

    def __init__(self, configs):
        self.detector = SolanaLaunchpadDetector(
            configs
        )

    def detect(
        self,
        observation: LaunchpadObservation,
    ) -> list[LaunchpadCandidate]:

        return self.detector.detect(
            observation
        )