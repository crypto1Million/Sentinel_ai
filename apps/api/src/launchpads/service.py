from __future__ import annotations

from chains.models import Chain

from launchpads.models import LaunchpadConfig
from launchpads.registry import (
    get_launchpad,
    get_launchpads,
)


class LaunchpadService:

    def list(
        self,
        chain: Chain | None = None,
    ) -> list[LaunchpadConfig]:
        return get_launchpads(
            chain=chain,
            active_only=True,
        )

    def resolve(
        self,
        chain: Chain,
        slug: str,
    ) -> LaunchpadConfig:
        return get_launchpad(
            chain=chain,
            slug=slug,
        )

    def serialize(
        self,
        launchpad: LaunchpadConfig,
    ) -> dict:
        return {
            "slug": launchpad.slug,
            "name": launchpad.name,
            "chain": launchpad.chain.value,
            "type": launchpad.launchpad_type.value,
            "website": launchpad.website,
            "discovery_method": (
                launchpad.discovery_method.value
            ),
            "active": launchpad.active,
            "program_ids": list(
                launchpad.program_ids
            ),
            "contract_addresses": list(
                launchpad.contract_addresses
            ),
            "notes": launchpad.notes,
        }