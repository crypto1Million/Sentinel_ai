from __future__ import annotations

from launchpads.attribution import (
    LaunchpadAttributor,
)

from launchpads.detectors.evm import (
    EVMLaunchpadDetector,
)

from launchpads.detectors.solana import (
    SolanaLaunchpadDetector,
)

from launchpads.models import (
    LaunchpadMatch,
    LaunchpadObservation,
)

from launchpads.registry import (
    get_enabled_launchpads_for_chain,
)

from chains.models import Chain


class LaunchpadAttributionService:

    def __init__(self) -> None:

        self.attributor = (
            LaunchpadAttributor()
        )

    def resolve(
        self,
        observation: LaunchpadObservation,
    ) -> LaunchpadMatch:

        try:
            chain = Chain(observation.chain)
        except ValueError:

            return LaunchpadMatch(
                status="UNAVAILABLE",
                chain=observation.chain,
                token_address=observation.token_address,
                reason=(
                    "Unsupported chain for launchpad "
                    "attribution."
                ),
                observed_at=observation.observed_at,
                transaction_signature=(
                    observation.transaction_signature
                ),
            )

        configs = (
            get_enabled_launchpads_for_chain(chain)
        )

        if chain == Chain.SOLANA:

            detector = SolanaLaunchpadDetector(
                configs
            )

        else:

            detector = EVMLaunchpadDetector(
                configs
            )

        candidates = detector.detect(
            observation
        )

        # ----------------------------------------------------------
        # Authoritative indexed partner metadata.
        #
        # This is intentionally exact.
        # It NEVER does:
        #   "Meteora => Jupiter"
        #   "Meteora => Believe"
        #   "Meteora => Bags"
        # ----------------------------------------------------------
        if observation.authoritative_partner_id:

            partner_id = (
                observation.authoritative_partner_id
            )

            partner_candidates = [

                config
                for config in configs
                if (
                    config.id == partner_id
                    and config.requires_authoritative_partner_metadata
                )
            ]

            for config in partner_candidates:

                # Only accept it when a real authoritative
                # partner mapping was supplied by upstream.
                candidates.append(
                    self._partner_candidate(
                        config,
                        observation,
                    )
                )

        return self.attributor.resolve(
            observation,
            candidates,
        )

    @staticmethod
    def _partner_candidate(
        config,
        observation,
    ):

        from launchpads.models import (
            EvidenceType,
            LaunchpadCandidate,
            LaunchpadEvidence,
        )

        return LaunchpadCandidate(
            launchpad_id=config.id,
            launchpad_name=config.name,
            chain=config.chain,
            matched_by=(
                config.detection_mode
            ),
            matched_value=(
                observation.authoritative_partner_id
                or config.id
            ),
            priority=config.priority,
            evidence=[
                LaunchpadEvidence(
                    evidence_type=(
                        EvidenceType.AUTHORITY_METADATA
                    ),
                    value=(
                        observation.authoritative_partner_id
                        or config.id
                    ),
                    chain=observation.chain,
                    transaction_signature=(
                        observation.transaction_signature
                    ),
                    block_number=(
                        observation.block_number
                    ),
                    slot=observation.slot,
                    source=observation.source,
                    observed_at=(
                        observation.observed_at
                    ),
                )
            ],
        )