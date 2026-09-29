from __future__ import annotations

from launchpads.detectors.evm import (
    EVMLaunchpadDetector,
)

from launchpads.models import (
    LaunchpadCandidate,
    LaunchpadObservation,
)


class ZoraDetector:

    def __init__(self, config):
        self.detector = EVMLaunchpadDetector(
            [config]
        )

    def detect(
        self,
        observation: LaunchpadObservation,
    ) -> list[LaunchpadCandidate]:

        return self.detector.detect(
            observation
        )