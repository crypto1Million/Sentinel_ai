"""
Jupiter Route Manager
=====================

Handles multi-hop routing, optimization, filtering,
and route scoring for Jupiter Aggregator.
"""

###############################################################################
# Imports
###############################################################################

from __future__ import annotations

from typing import Dict, List, Optional

###############################################################################
# RouteManager
###############################################################################


class RouteManager:
    """
    Jupiter Multi-Hop Route Engine.
    """

    ###########################################################################
    # Initialization
    ###########################################################################

    def __init__(self):

        self.routes: List[Dict] = []

    ###########################################################################
    # Route Management
    ###########################################################################

    def route(
        self,
        route: Dict,
    ) -> Dict:

        return normalize_route(route)

    ###########################################################################

    def routes_list(
        self,
        routes: List[Dict],
    ) -> List[Dict]:

        self.routes = [
            normalize_route(r)
            for r in routes
        ]

        return self.routes

    ###########################################################################

    def best_route(
        self,
        routes: Optional[List[Dict]] = None,
    ) -> Dict:

        routes = routes or self.routes

        if not routes:

            return {}

        return max(
            routes,
            key=lambda r: float(
                r.get(
                    "out_amount",
                    0,
                )
            ),
        )

    ###########################################################################

    def cheapest_route(
        self,
        routes: Optional[List[Dict]] = None,
    ) -> Dict:

        routes = routes or self.routes

        if not routes:

            return {}

        return min(
            routes,
            key=lambda r: float(
                r.get(
                    "price_impact",
                    0,
                )
            ),
        )

    ###########################################################################

    def route_hops(
        self,
        route: Dict,
    ) -> List[Dict]:

        return route.get(
            "route_plan",
            [],
        )

    ###########################################################################

    def route_statistics(
        self,
        routes: Optional[List[Dict]] = None,
    ) -> Dict:

        routes = routes or self.routes

        if not routes:

            return {}

        return {
            "total_routes": len(routes),
            "best_output": self.best_route(routes).get(
                "out_amount"
            ),
            "lowest_impact": self.cheapest_route(routes).get(
                "price_impact"
            ),
        }

    ###########################################################################

    def route_score(
        self,
        route: Dict,
    ) -> float:

        impact = float(
            route.get(
                "price_impact",
                0,
            )
        )

        hops = len(
            route.get(
                "route_plan",
                [],
            )
        )

        score = 100

        score -= impact * 100

        score -= hops * 2

        return round(
            max(score, 0),
            2,
        )

    ###########################################################################
    # Filters
    ###########################################################################

    def filter_by_hops(
        self,
        max_hops: int,
    ) -> List[Dict]:

        return [
            r
            for r in self.routes
            if len(
                r.get(
                    "route_plan",
                    [],
                )
            )
            <= max_hops
        ]

    ###########################################################################

    def filter_by_price_impact(
        self,
        maximum: float,
    ) -> List[Dict]:

        return [
            r
            for r in self.routes
            if float(
                r.get(
                    "price_impact",
                    0,
                )
            )
            <= maximum
        ]

    ###########################################################################
    # Runtime
    ###########################################################################

    def diagnostics(self):

        return {
            "manager": "RouteManager",
            "cached_routes": len(self.routes),
        }

    ###########################################################################

    def summary(self):

        return {
            "provider": "Jupiter",
            "component": "Route Manager",
        }


###############################################################################
# Utilities
###############################################################################


def normalize_route(
    route: Dict,
) -> Dict:

    return {
        "input_mint": route.get(
            "inputMint"
        ),
        "output_mint": route.get(
            "outputMint"
        ),
        "in_amount": float(
            route.get(
                "inAmount",
                0,
            )
        ),
        "out_amount": float(
            route.get(
                "outAmount",
                0,
            )
        ),
        "price_impact": float(
            route.get(
                "priceImpactPct",
                0,
            )
        ),
        "route_plan": route.get(
            "routePlan",
            [],
        ),
    }


###############################################################################


def route_metadata(
    route: Dict,
) -> Dict:

    return {
        "input": route.get("inputMint"),
        "output": route.get("outputMint"),
        "hops": len(
            route.get(
                "routePlan",
                [],
            )
        ),
    }