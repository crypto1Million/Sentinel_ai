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


class SolanaLaunchpadDetector(
    LaunchpadDetector
):

    def detect(
        self,
        observation: LaunchpadObservation,
    ) -> list[LaunchpadCandidate]:

        candidates: list[LaunchpadCandidate] = []

        observed_programs = set(
            observation.program_ids
        )

        observed_config = (
            observation.platform_config_address
        )

        for config in self.configs:

            matched_program: str | None = None

            for program_id in config.program_ids:

                if program_id in observed_programs:
                    matched_program = program_id
                    break

            if matched_program is None:
                continue

            # ------------------------------------------------------
            # Specialized platform-config match.
            # ------------------------------------------------------
            if config.platform_config_addresses:

                if (
                    observed_config is not None
                    and observed_config
                    in config.platform_config_addresses
                ):
                    evidence = [
                        LaunchpadEvidence(
                            evidence_type=(
                                EvidenceType.PROGRAM_ID
                            ),
                            value=matched_program,
                            chain=observation.chain,
                            transaction_signature=(
                                observation.transaction_signature
                            ),
                            slot=observation.slot,
                            source=observation.source,
                            observed_at=(
                                observation.observed_at
                            ),
                        ),
                        LaunchpadEvidence(
                            evidence_type=(
                                EvidenceType.PLATFORM_CONFIG
                            ),
                            value=observed_config,
                            chain=observation.chain,
                            transaction_signature=(
                                observation.transaction_signature
                            ),
                            slot=observation.slot,
                            source=observation.source,
                            observed_at=(
                                observation.observed_at
                            ),
                        ),
                    ]

                    candidates.append(
                        LaunchpadCandidate(
                            launchpad_id=config.id,
                            launchpad_name=config.name,
                            chain=config.chain,
                            matched_by=(
                                DetectionMode.PLATFORM_CONFIG
                            ),
                            matched_value=observed_config,
                            priority=config.priority,
                            evidence=evidence,
                        )
                    )

                # Config exists but wasn't observed.
                # Do NOT guess the brand.
                continue

            # ------------------------------------------------------
            # Generic program / shared-rail match.
            # ------------------------------------------------------

            evidence = [
                LaunchpadEvidence(
                    evidence_type=(
                        EvidenceType.PROGRAM_ID
                    ),
                    value=matched_program,
                    chain=observation.chain,
                    transaction_signature=(
                        observation.transaction_signature
                    ),
                    slot=observation.slot,
                    source=observation.source,
                    observed_at=(
                        observation.observed_at
                    ),
                )
            ]

            candidates.append(
                LaunchpadCandidate(
                    launchpad_id=config.id,
                    launchpad_name=config.name,
                    chain=config.chain,
                    matched_by=config.detection_mode,
                    matched_value=matched_program,
                    priority=config.priority,
                    evidence=evidence,
                )
            )

        return candidates