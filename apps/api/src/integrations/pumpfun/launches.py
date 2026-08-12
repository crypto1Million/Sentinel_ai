"""
Pump.fun Launch Monitor
=======================

Monitors newly launched Pump.fun tokens.
"""

###############################################################################
# Imports
###############################################################################

from __future__ import annotations

from typing import Dict, List

###############################################################################
# LaunchMonitor
###############################################################################


class LaunchMonitor:
    """
    Pump.fun Launch Monitor.
    """

    ###########################################################################
    # Monitoring
    ###########################################################################

    def latest_launches(
        self,
        launches: List[Dict],
    ) -> List[Dict]:

        return [
            normalize_launch(i)
            for i in launches
        ]

    ###########################################################################

    def stream_launches(
        self,
        launches: List[Dict],
    ):

        for launch in launches:

            yield normalize_launch(
                launch
            )

    ###########################################################################

    def new_launch(
        self,
        launch: Dict,
    ) -> Dict:

        return normalize_launch(
            launch
        )

    ###########################################################################

    def launch_statistics(
        self,
        launches: List[Dict],
    ) -> Dict:

        return {
            "total_launches": len(launches),
            "average_marketcap": (
                sum(
                    i.get("market_cap", 0)
                    for i in launches
                )
                / max(len(launches), 1)
            ),
        }

    ###########################################################################

    def migration_events(
        self,
        launches: List[Dict],
    ) -> List[Dict]:

        return [
            launch
            for launch in launches
            if launch.get("migrated")
        ]

    ###########################################################################

    def diagnostics(self):

        return {
            "monitor": "Pump.fun",
            "status": "healthy",
        }

    ###########################################################################
    # Filtering
    ###########################################################################

    def filter_by_marketcap(
        self,
        launches: List[Dict],
        minimum: float = 0,
        maximum: float = 1_000_000,
    ) -> List[Dict]:

        return [
            launch
            for launch in launches
            if minimum
            <= launch.get("market_cap", 0)
            <= maximum
        ]

    ###########################################################################

    def filter_by_volume(
        self,
        launches: List[Dict],
        minimum: float,
    ) -> List[Dict]:

        return [
            launch
            for launch in launches
            if launch.get("volume", 0)
            >= minimum
        ]

    ###########################################################################

    def filter_by_liquidity(
        self,
        launches: List[Dict],
        minimum: float,
    ) -> List[Dict]:

        return [
            launch
            for launch in launches
            if launch.get("liquidity", 0)
            >= minimum
        ]

    ###########################################################################

    def filter_by_deployer(
        self,
        launches: List[Dict],
        wallet: str,
    ) -> List[Dict]:

        return [
            launch
            for launch in launches
            if launch.get("creator")
            == wallet
        ]

    ###########################################################################

    def filter_verified(
        self,
        launches: List[Dict],
    ) -> List[Dict]:

        return [
            launch
            for launch in launches
            if launch.get("verified")
        ]

    ###########################################################################
    # Runtime
    ###########################################################################

    def summary(self):

        return {
            "service": "Launch Monitor",
            "provider": "Pump.fun",
        }


###############################################################################
# Utilities
###############################################################################


def normalize_launch(
    launch: Dict,
) -> Dict:

    return {
        "mint": launch.get("mint"),
        "name": launch.get("name"),
        "symbol": launch.get("symbol"),
        "creator": launch.get("creator"),
        "market_cap": launch.get("market_cap"),
        "volume": launch.get("volume"),
        "liquidity": launch.get("liquidity"),
        "verified": launch.get("verified", False),
        "migrated": launch.get("migrated", False),
        "created_at": launch.get("created_at"),
    }


###############################################################################


def launch_metadata(
    launch: Dict,
) -> Dict:

    return {
        "mint": launch.get("mint"),
        "creator": launch.get("creator"),
        "timestamp": launch.get("created_at"),
    }