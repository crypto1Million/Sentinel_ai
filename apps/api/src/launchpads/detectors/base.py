from __future__ import annotations

from abc import ABC, abstractmethod

from launchpads.models import (
    LaunchpadCandidate,
    LaunchpadConfig,
    LaunchpadObservation,
)


class LaunchpadDetector(ABC):

    def __init__(
        self,
        configs: list[LaunchpadConfig],
    ) -> None:
        self.configs = configs

    @abstractmethod
    def detect(
        self,
        observation: LaunchpadObservation,
    ) -> list[LaunchpadCandidate]:
        raise NotImplementedError