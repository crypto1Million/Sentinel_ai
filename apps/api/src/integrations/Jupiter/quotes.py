"""
Jupiter Quote Manager
=====================

Quote engine and price estimation layer.
"""

###############################################################################
# Imports
###############################################################################

from __future__ import annotations

from typing import Dict, List

###############################################################################
# QuoteManager
###############################################################################


class QuoteManager:
    """
    Jupiter Quote Engine.
    """

    ###########################################################################
    # Quotes
    ###########################################################################

    def quote(
        self,
        quote: Dict,
    ) -> Dict:

        return normalize_quote(quote)

    ###########################################################################

    def best_quote(
        self,
        quotes: List[Dict],
    ) -> Dict:

        if not quotes:

            return {}

        return max(
            quotes,
            key=lambda q: float(
                q.get("out_amount", 0)
            ),
        )

    ###########################################################################

    def estimate_price(
        self,
        quote: Dict,
    ) -> float:

        amount_in = float(
            quote.get("in_amount", 0)
        )

        amount_out = float(
            quote.get("out_amount", 0)
        )

        if amount_in == 0:

            return 0

        return amount_out / amount_in

    ###########################################################################

    def estimate_output(
        self,
        quote: Dict,
    ) -> float:

        return float(
            quote.get("out_amount", 0)
        )

    ###########################################################################

    def estimate_price_impact(
        self,
        quote: Dict,
    ) -> float:

        return float(
            quote.get(
                "price_impact_pct",
                0,
            )
        )

    ###########################################################################

    def estimate_slippage(
        self,
        quote: Dict,
    ) -> float:

        return float(
            quote.get(
                "slippage_bps",
                0,
            )
        )

    ###########################################################################

    def quote_statistics(
        self,
        quotes: List[Dict],
    ) -> Dict:

        if not quotes:

            return {}

        impacts = [
            self.estimate_price_impact(q)
            for q in quotes
        ]

        return {
            "quotes": len(quotes),
            "best_output": self.best_quote(
                quotes
            ).get("out_amount"),
            "average_price_impact": (
                sum(impacts) / len(impacts)
            ),
        }

    ###########################################################################

    def quote_score(
        self,
        quote: Dict,
    ) -> float:

        impact = self.estimate_price_impact(
            quote
        )

        score = max(
            0,
            100 - impact * 100,
        )

        return round(score, 2)

    ###########################################################################
    # Runtime
    ###########################################################################

    def summary(self):

        return {
            "engine": "QuoteManager",
            "provider": "Jupiter",
        }


###############################################################################
# Utilities
###############################################################################


def normalize_quote(
    quote: Dict,
) -> Dict:

    return {
        "input_mint": quote.get(
            "inputMint"
        ),
        "output_mint": quote.get(
            "outputMint"
        ),
        "in_amount": float(
            quote.get(
                "inAmount",
                0,
            )
        ),
        "out_amount": float(
            quote.get(
                "outAmount",
                0,
            )
        ),
        "price_impact_pct": float(
            quote.get(
                "priceImpactPct",
                0,
            )
        ),
        "slippage_bps": int(
            quote.get(
                "slippageBps",
                0,
            )
        ),
        "route": quote.get(
            "routePlan",
            [],
        ),
    }


###############################################################################


def quote_metadata(
    quote: Dict,
) -> Dict:

    return {
        "input": quote.get("inputMint"),
        "output": quote.get("outputMint"),
        "routes": len(
            quote.get(
                "routePlan",
                [],
            )
        ),
    }