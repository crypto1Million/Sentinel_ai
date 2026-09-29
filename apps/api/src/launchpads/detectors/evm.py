from __future__ import annotations

from launchpads.detectors.base import (
    LaunchpadDetector,
)

from launchpads.models import (
    DetectionMode,
    EvidenceType,
    LaunchpadCandidate,
    LaunchpadEvidence,
    LaunchpadObservation,
)


class EVMLaunchpadDetector(
    LaunchpadDetector
):

    def detect(
        self,
        observation: LaunchpadObservation,
    ) -> list[LaunchpadCandidate]:

        candidates: list[LaunchpadCandidate] = []

        if observation.factory_address is None:
            return candidates

        observed_factory = (
            observation.factory_address.lower()
        )

        for config in self.configs:

            configured_factories = {
                address.lower()
                for address in config.factory_addresses
            }

            if observed_factory not in configured_factories:
                continue

            evidence = [
                LaunchpadEvidence(
                    evidence_type=(
                        EvidenceType.FACTORY_ADDRESS
                    ),
                    value=observed_factory,
                    chain=observation.chain,
                    transaction_signature=(
                        observation.transaction_signature
                    ),
                    block_number=(
                        observation.block_number
                    ),
                    source=observation.source,
                    observed_at=(
                        observation.observed_at
                    ),
                )
            ]

            if observation.event_name:

                if config.event_names:

                    if (
                        observation.event_name
                        not in config.event_names
                    ):
                        continue

                    evidence.append(
                        LaunchpadEvidence(
                            evidence_type=(
                                EvidenceType.EVENT
                            ),
                            value=(
                                observation.event_name
                            ),
                            chain=observation.chain,
                            transaction_signature=(
                                observation.transaction_signature
                            ),
                            block_number=(
                                observation.block_number
                            ),
                            source=observation.source,
                            observed_at=(
                                observation.observed_at
                            ),
                        )
                    )

            candidates.append(
                LaunchpadCandidate(
                    launchpad_id=config.id,
                    launchpad_name=config.name,
                    chain=config.chain,
                    matched_by=(
                        DetectionMode.EXACT_FACTORY
                    ),
                    matched_value=observed_factory,
                    priority=config.priority,
                    evidence=evidence,
                )
            )

        return candidates