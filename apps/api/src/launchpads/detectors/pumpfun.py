from __future__ import annotations

from launchpads.detectors.solana import (
    SolanaLaunchpadDetector,
)

from launchpads.models import LaunchpadCandidate, LaunchpadObservation


class PumpFunDetector:

    def __init__(self, config):
        self.detector = SolanaLaunchpadDetector(
            [config]
        )

    def detect(
        self,
        observation: LaunchpadObservation,
    ) -> list[LaunchpadCandidate]:

        return self.detector.detect(
            observation
        )