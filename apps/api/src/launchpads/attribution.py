from __future__ import annotations

from launchpads.models import (
    LaunchpadCandidate,
    LaunchpadMatch,
    LaunchpadObservation,
    LaunchpadStatus,
)


class LaunchpadAttributor:

    def resolve(
        self,
        observation: LaunchpadObservation,
        candidates: list[LaunchpadCandidate],
    ) -> LaunchpadMatch:

        # ----------------------------------------------------------
        # No evidence at all.
        # ----------------------------------------------------------
        if not candidates:

            return LaunchpadMatch(
                status=LaunchpadStatus.NOT_FOUND,
                chain=observation.chain,
                token_address=observation.token_address,
                evidence=observation.evidence,
                reason=(
                    "No deterministic launchpad evidence "
                    "was found."
                ),
                observed_at=observation.observed_at,
                transaction_signature=(
                    observation.transaction_signature
                ),
            )

        # ----------------------------------------------------------
        # Highest priority evidence wins ONLY when it is unique.
        # ----------------------------------------------------------
        highest_priority = max(
            candidate.priority
            for candidate in candidates
        )

        top = [
            candidate
            for candidate in candidates
            if candidate.priority == highest_priority
        ]

        # Same launchpad may be reported by multiple evidence paths.
        unique_launchpads = {
            candidate.launchpad_id
            for candidate in top
        }

        if len(unique_launchpads) == 1:

            selected = top[0]

            return LaunchpadMatch(
                status=LaunchpadStatus.VERIFIED,
                chain=observation.chain,
                token_address=observation.token_address,
                launchpad_id=selected.launchpad_id,
                launchpad_name=selected.launchpad_name,
                rail_id=(
                    selected.matched_value
                    if selected.matched_by.value
                    == "SHARED_RAIL"
                    else None
                ),
                candidates=candidates,
                evidence=(
                    selected.evidence
                    + observation.evidence
                ),
                reason=(
                    f"Deterministic evidence matched "
                    f"{selected.launchpad_name}."
                ),
                observed_at=observation.observed_at,
                transaction_signature=(
                    observation.transaction_signature
                ),
            )

        # ----------------------------------------------------------
        # Multiple independent brands match at the same priority.
        # Never pick one arbitrarily.
        # ----------------------------------------------------------
        return LaunchpadMatch(
            status=LaunchpadStatus.CONFLICT,
            chain=observation.chain,
            token_address=observation.token_address,
            candidates=candidates,
            evidence=observation.evidence,
            reason=(
                "Multiple launchpad candidates matched with "
                "equal attribution priority."
            ),
            observed_at=observation.observed_at,
            transaction_signature=(
                observation.transaction_signature
            ),
        )