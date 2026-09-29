from __future__ import annotations

from launchpads.detectors.evm import (
    EVMLaunchpadDetector,
)

from launchpads.models import (
    LaunchpadCandidate,
    LaunchpadObservation,
)


class UniswapLaunchDetector:

    def __init__(self, configs):
        self.detector = EVMLaunchpadDetector(
            configs
        )

    def detect(
        self,
        observation: LaunchpadObservation,
    ) -> list[LaunchpadCandidate]:

        return self.detector.detect(
            observation
        )